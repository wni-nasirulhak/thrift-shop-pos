"""
pages/pos.py — Point of Sale integrated with React UI.
"""

import streamlit as st
import time
from datetime import datetime
from src.database.inventory import load_all_inventory
from src.database.customers import load_all_customers
from src.database.sales import record_sale
from src.components.react_pos import render_react_pos
from src.components.ui_helpers import render_receipt

def render(sheet):
    st.markdown('<div class="pos-app-wrapper">', unsafe_allow_html=True)
    
    with st.spinner("⏳ กำลังโหลดข้อมูลร้านค้า..."):
        # Load all data for React
        inv_df = load_all_inventory(sheet)
        inventory_records = inv_df.to_dict('records') if not inv_df.empty else []
        customers_records = load_all_customers(sheet)

    # Render React POS component
    payload = render_react_pos(
        inventory=inventory_records,
        customers=customers_records,
        key="pos_main"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Process Checkout Payload
    if payload and payload.get("cart"):
        process_checkout(sheet, payload)

def process_checkout(sheet, payload: dict):
    # --- 1. Prevent Infinite Loop ---
    checkout_id = payload.get("checkoutId")
    if not checkout_id:
        return
    
    if "processed_checkouts" not in st.session_state:
        st.session_state.processed_checkouts = set()
        
    if checkout_id in st.session_state.processed_checkouts:
        return # Skip processing if already done
        
    st.session_state.processed_checkouts.add(checkout_id)

    # --- 2. Extract Payload ---
    cart = payload.get("cart", [])
    customer = payload.get("customer")
    new_customer_name = payload.get("newCustomerName", "").strip()
    customer_address = payload.get("customerAddress", "").strip()
    customer_phone_search = payload.get("customerPhone", "").strip()
    
    discount_type = payload.get("discountType", "none")
    discount_amount = float(payload.get("discountAmount", 0))
    cart_final_price = float(payload.get("finalPrice", 0))
    payment_method = payload.get("paymentMethod", "Cash")
    points_used = int(payload.get("pointsUsed", 0))
    
    # Resolve customer phone: use selected customer or the typed phone
    customer_phone = str(customer["Phone_Number"]) if customer else customer_phone_search

    # --- 3. Process Logic ---
    with st.spinner("⏳ กำลังบันทึกการขาย..."):
        # Auto-register new customer if provided
        from src.database.customers import register_customer
        if not customer and customer_phone and new_customer_name:
            register_customer(sheet, customer_phone, new_customer_name)
            
        success_count = 0
        total_original = sum(float(c.get("Price", 0)) for c in cart)
        
        for idx, item in enumerate(cart):
            is_first = (idx == 0)
            item_price = float(item.get("Price", 0))
            
            # สัดส่วนของสินค้านี้คิดเป็นกี่ % ของราคารวม
            ratio = item_price / total_original if total_original > 0 else 0
            
            i_final_price = cart_final_price * ratio
            i_discount_val = (item_price - i_final_price)
            i_points_used = points_used if is_first else 0 
            
            ok = record_sale(
                sheet=sheet,
                barcode_id=item["Barcode_ID"],
                original_price=item_price,
                discount_type=discount_type if is_first else "รวมกับรายการอื่น",
                discount_value=i_discount_val,
                final_price=i_final_price,
                payment_method=payment_method,
                customer_phone=customer_phone,
                points_used=i_points_used,
            )
            
            # If an address is provided, log it into Shipping
            if ok and customer_address:
                from src.database.shipping import record_shipping
                record_shipping(sheet, item["Barcode_ID"], customer_address, tracking_no="รอดำเนินการ", status="Reserved")
                
            if ok:
                success_count += 1
                
        if success_count == len(cart):
            st.toast("✅ บันทึกการขายสำเร็จ!", icon="🛒")
            
            item_names = ", ".join([c["Item_Name"] for c in cart])
            render_receipt(
                item_name=item_names[:50] + ("..." if len(item_names) > 50 else ""),
                price=total_original,
                discount_amount=discount_amount + points_used,
                final_price=cart_final_price,
                payment=payment_method,
                timestamp=datetime.now().strftime("%d/%m/%Y %H:%M")
            )
            time.sleep(3)
            # Important: Clear the payload or reset to avoid stale data
            st.rerun()
        else:
            st.error("❌ บันทึกการขายบางรายการไม่สำเร็จ")

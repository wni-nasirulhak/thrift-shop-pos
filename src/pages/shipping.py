"""
pages/shipping.py — Manage ready-to-ship orders
"""

import streamlit as st
from src.database.inventory import load_all_inventory, find_item_by_barcode
from src.database.shipping import record_shipping
from src.components.ui_helpers import render_section, render_empty_state, render_divider

def render(sheet):
    render_section("🚚 จัดส่งพัสดุ (Shipping)")

    df = load_all_inventory(sheet)
    if df.empty:
        render_empty_state("📦", "ไม่มีรายการสินค้า")
        return

    # Filter items that are sold but not shipped yet
    # Assuming "Sold" means sold at POS, and "Shipped" means it has been sent
    pending_df = df[df["Status"].isin(["Sold", "Reserved"])].copy()
    
    if pending_df.empty:
        render_empty_state("✅", "ไม่มีพัสดุเตรียมจัดส่งในขณะนี้")
        return

    st.markdown("### 📋 รายการรอจัดส่ง")
    options = []
    option_map = {}
    for idx, row in pending_df.iterrows():
        barcode = row.get("Barcode_ID", "")
        name = row.get("Item_Name", "")
        status = row.get("Status", "")
        label = f"[{status}] {barcode} - {name}"
        options.append(label)
        option_map[label] = barcode

    selected_label = st.selectbox("เลือกสินค้าที่ต้องการจัดส่ง", options)
    
    if selected_label:
        barcode_id = option_map[selected_label]
        render_divider()
        st.markdown(f"**กรอกข้อมูลจัดส่งสำหรับ:** `{barcode_id}`")
        
        item = find_item_by_barcode(sheet, barcode_id)
        if item:
            with st.form(key=f"shipping_form_{barcode_id}"):
                address = st.text_area("ที่อยู่จัดส่ง", placeholder="บ้านเลขที่ ตำบล อำเภอ จังหวัด รหัสไปรษณีย์")
                tracking_no = st.text_input("เลขพัสดุ (Tracking No.)", placeholder="เช่น TH0123456789")
                
                col1, col2 = st.columns(2)
                with col1:
                    print_btn = st.form_submit_button("🖨️ พิมพ์ใบปะหน้า (จำลอง)")
                with col2:
                    submit_btn = st.form_submit_button("✅ ยืนยันการจัดส่ง", type="primary")
                    
                if print_btn:
                    if not address:
                        st.error("กรุณากรอกที่อยู่เพื่อพิมพ์ใบปะหน้า")
                    else:
                        st.info("จำลองการพิมพ์ใบปะหน้า: สามารถเชื่อม API ขนส่งหรือพิมพ์สติ๊กเกอร์ได้ที่นี่")
                        st.code(f"ผู้รับ:\n{address}\nเลขพัสดุ: {tracking_no or 'N/A'}\nสินค้า: {item.get('Item_Name')}", language="text")
                        
                if submit_btn:
                    if not address:
                        st.error("กรุณากรอกที่อยู่จัดส่ง")
                    else:
                        with st.spinner("⏳ กำลังบันทึกสถานะจัดส่ง..."):
                            if record_shipping(sheet, barcode_id, address, tracking_no, status="Shipped"):
                                st.success("อัปเดตสถานะเป็น 'จัดส่งแล้ว' สำเร็จ!")
                                st.balloons()
                                st.rerun()

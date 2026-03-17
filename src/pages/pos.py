"""
pages/pos.py — Point of Sale: scan barcode, apply discount, record sale.
"""

import streamlit as st
import time
from datetime import datetime
from src.config import PAYMENT_OPTIONS
from src.database.inventory import find_item_by_barcode
from src.database.measurements import load_measurements
from src.database.sales import record_sale
from src.services.images import decode_base64_to_bytes
from src.components.ui_helpers import (
    render_section, render_divider,
    render_item_card, render_price_box, render_receipt,
)


def render(sheet):
    render_section("🛒 สแกนสินค้าเพื่อขาย")

    barcode_input = st.text_input(
        "รหัสสินค้า",
        placeholder="พิมพ์หรือสแกนบาร์โค้ด เช่น UNIQLO-SH-001",
        help="กรอกรหัสแล้วกด Enter",
        label_visibility="collapsed",
    )

    if not barcode_input:
        return

    with st.spinner("🔍 กำลังค้นหา..."):
        item = find_item_by_barcode(sheet, barcode_input)

    if not item:
        st.error("❌ ไม่พบสินค้ารหัสนี้ในระบบ")
        return

    if item.get("Status") == "Sold":
        st.error("❌ สินค้านี้ขายไปแล้ว!")
        return

    st.success("✅ พบสินค้า!")

    # โหลดขนาด (ถ้ามี)
    item["measurements"] = load_measurements(sheet, item.get("Category_ID", ""), barcode_input)

    price    = float(item.get("Price", 0) or 0)
    cost_val = float(item.get("Cost",  0) or 0)

    # ===== รูปสินค้า =====
    photo_bytes = decode_base64_to_bytes(item.get("Photo", ""))
    if photo_bytes:
        st.markdown("**📷 รูปสินค้า**")
        col_p, _, _ = st.columns([1, 1, 2])
        with col_p:
            st.image(photo_bytes, use_container_width=True)

    # ===== ข้อมูลสินค้า + ราคา =====
    col1, col2 = st.columns([3, 2])
    with col1:
        render_item_card(item)
        meas = item.get("measurements", {})
        meas_items = [(k, v) for k, v in meas.items() if k not in ("Barcode_ID", "Updated_Date") and v]
        if meas_items:
            with st.expander("📏 ขนาดจริง"):
                for k, v in meas_items:
                    st.text(f"• {k}: {v}")
    with col2:
        render_price_box(price, cost_val)

    render_divider()

    # ===== ส่วนลด =====
    st.markdown("**🏷️ ส่วนลด**")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        discount_type = st.radio(
            "ประเภทส่วนลด",
            ["ไม่มี", "เปอร์เซ็นต์ (%)", "บาท (฿)"],
            label_visibility="collapsed",
        )
    with col_d2:
        if discount_type == "เปอร์เซ็นต์ (%)":
            disc_pct    = st.number_input("ส่วนลด (%)", 0.0, 100.0, step=1.0)
            disc_amount = price * disc_pct / 100
            disc_value  = disc_pct
        elif discount_type == "บาท (฿)":
            disc_amount = st.number_input("ส่วนลด (฿)", 0.0, float(price), step=1.0)
            disc_value  = 0.0
        else:
            disc_amount = 0.0
            disc_value  = 0.0

    final_price = price - disc_amount

    if disc_amount > 0:
        st.markdown(
            f'<div class="discount-badge">🏷️ ส่วนลด -฿{disc_amount:,.2f} → ราคาสุดท้าย '
            f'<strong>฿{final_price:,.2f}</strong></div>',
            unsafe_allow_html=True,
        )

    payment = st.selectbox("💳 วิธีชำระเงิน", PAYMENT_OPTIONS)

    # ===== Confirm =====
    if st.button("✅ ยืนยันการขาย", use_container_width=True, type="primary"):
        with st.spinner("⏳ กำลังบันทึก..."):
            ok = record_sale(
                sheet, barcode_input, price,
                discount_type, disc_value, final_price,
                payment.split(" ", 1)[-1],  # strip emoji
            )

        if ok:
            st.balloons()
            render_receipt(
                item_name=item.get("Item_Name", ""),
                price=price,
                discount_amount=disc_amount,
                final_price=final_price,
                payment=payment,
                timestamp=datetime.now().strftime("%d/%m/%Y %H:%M"),
            )
            time.sleep(3)
            st.rerun()

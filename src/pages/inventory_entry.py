"""
pages/inventory_entry.py — Add new items to inventory.
Steps: 1) Category → 2) Item info → 3) Measurements → 4) Photo → Save
"""

import streamlit as st
from src.config import SIZE_OPTIONS, CONDITION_OPTIONS, MEASUREMENT_FIELDS
from src.database.catalog import get_active_categories, get_active_brand_names, get_brand_code
from src.database.inventory import add_inventory_item
from src.database.measurements import save_measurements
from src.services.barcode import generate_barcode_id, generate_qr_bytes
from src.services.images import compress_to_base64, decode_base64_to_bytes, estimate_size_kb
from src.components.ui_helpers import (
    render_section, render_divider, render_barcode_preview,
    render_qr_result, render_profit_hint,
)


def render(sheet, categories_df, brands_df):
    if categories_df.empty or brands_df.empty:
        st.error("❌ ไม่พบข้อมูล Categories หรือ Brands")
        if st.button("🔄 ลองโหลดใหม่"):
            st.cache_data.clear()
            st.rerun()
        return

    # ===== Step 1: Category =====
    render_section("เลือกหมวดหมู่สินค้า", step=1)
    cat_options = get_active_categories(categories_df)
    selected_display = st.selectbox("หมวดหมู่ *", list(cat_options.keys()), label_visibility="collapsed")
    selected_cat  = cat_options[selected_display]
    category_id   = selected_cat["Category_ID"]
    category_name = selected_cat["Category_Name"]
    category_code = selected_cat["Code_Prefix"]

    render_divider()

    # ===== Step 2: Item Info =====
    render_section("ข้อมูลสินค้า", step=2)

    col1, col2 = st.columns(2)
    with col1:
        brand_names   = get_active_brand_names(brands_df)
        selected_brand = st.selectbox("🏷️ แบรนด์ *", brand_names)
        brand_code    = get_brand_code(brands_df, selected_brand)
        item_name     = st.text_input("📝 ชื่อสินค้า *", placeholder="เช่น เสื้อยืดสีขาว Uniqlo")
        size_label    = st.selectbox("📐 ไซส์ป้าย", SIZE_OPTIONS)

    with col2:
        condition = st.selectbox("⭐ สภาพสินค้า *", CONDITION_OPTIONS)
        color     = st.text_input("🎨 สี", placeholder="ขาว, ดำ, ลายดอก")
        pattern   = st.text_input("🖼️ ลวดลาย", placeholder="ลายทาง, เรียบ")

    material = st.text_input("🧵 วัสดุ/ผ้า", placeholder="ฝ้าย 100%, โพลีเอสเตอร์")

    col3, col4 = st.columns(2)
    with col3:
        cost  = st.number_input("💸 ต้นทุน (฿) *",  min_value=0.0, step=1.0)
    with col4:
        price = st.number_input("💰 ราคาขาย (฿) *", min_value=0.0, step=1.0)

    render_profit_hint(cost, price)
    render_divider()

    # ===== Step 3: Measurements =====
    render_section(f"วัดขนาด {category_name}", step=3)
    measurements_data = _render_measurements(category_id)
    render_divider()

    # ===== Barcode Preview =====
    if brand_code and category_code:
        preview_id = generate_barcode_id(brand_code, category_code, sheet)
        render_barcode_preview(preview_id)

    render_divider()

    # ===== Step 4: Photo =====
    render_section("รูปสินค้า (ไม่บังคับ)", step=4)
    photo_b64 = _render_photo_uploader()

    # ===== Save =====
    render_divider()
    if st.button("✅ บันทึกสินค้าเข้าสต็อก", use_container_width=True, type="primary"):
        _handle_save(
            sheet, brand_code, category_code, category_id, category_name,
            item_name, selected_brand, size_label, condition,
            color, pattern, material, cost, price,
            measurements_data, photo_b64,
        )


# ===== Private helpers =====

def _render_measurements(category_id: str) -> dict:
    """แสดง measurement fields ตาม category และคืน dict ค่า."""
    fields_def = MEASUREMENT_FIELDS.get(category_id)
    if not fields_def:
        st.info("💡 หมวดหมู่นี้ไม่ต้องวัดขนาดเพิ่มเติม")
        return {}

    data = {}
    st.markdown('<div class="measurement-card">', unsafe_allow_html=True)
    st.caption("📏 กรอกขนาดจริงของสินค้า (ซม.) — ถ้าไม่มีให้ใส่ 0")

    labels = fields_def.get("labels", {})

    # Numeric fields — show in 2 columns
    numeric_fields = fields_def.get("numeric", [])
    if numeric_fields:
        cols = st.columns(2)
        for i, key in enumerate(numeric_fields):
            label = labels.get(key, key)
            with cols[i % 2]:
                data[key] = st.number_input(label, min_value=0.0, step=0.5, key=f"m_{key}")

    # Text fields (shoes size strings)
    text_fields = fields_def.get("text", [])
    if text_fields:
        cols = st.columns(2)
        for i, key in enumerate(text_fields):
            label = labels.get(key, key)
            with cols[i % 2]:
                data[key] = st.text_input(label, key=f"m_{key}")

    # Select fields
    select_fields = fields_def.get("select", {})
    if select_fields:
        sel_cols = st.columns(len(select_fields))
        for i, (key, options) in enumerate(select_fields.items()):
            label = labels.get(key, key)
            with sel_cols[i]:
                data[key] = st.selectbox(label, options, key=f"m_{key}")

    st.markdown('</div>', unsafe_allow_html=True)
    return data


def _render_photo_uploader() -> str:
    """แสดง file uploader และคืน base64 string."""
    uploaded = st.file_uploader(
        "อัปโหลดรูปสินค้า",
        type=["jpg", "jpeg", "png", "webp"],
        help="รูปจะถูกบีบอัดอัตโนมัติ (max 400×400px)",
        label_visibility="collapsed",
    )
    if not uploaded:
        return ""

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(uploaded, caption="Preview", use_container_width=True)
    with col2:
        b64 = compress_to_base64(uploaded)
        if b64:
            kb = estimate_size_kb(b64)
            st.success(f"✅ รูปพร้อมบันทึก ({kb:.0f} KB)")
        else:
            st.error("❌ แปลงรูปไม่สำเร็จ ลองใหม่")
        return b64
    return ""


def _handle_save(
    sheet, brand_code, category_code, category_id, category_name,
    item_name, brand, size_label, condition,
    color, pattern, material, cost, price,
    measurements_data, photo_b64,
):
    if not item_name:
        st.error("❌ กรุณากรอกชื่อสินค้า")
        return
    if cost <= 0 or price <= 0:
        st.error("❌ ต้นทุนและราคาต้องมากกว่า 0")
        return

    barcode_id = generate_barcode_id(brand_code, category_code, sheet)

    with st.spinner("⏳ กำลังบันทึก..."):
        ok = add_inventory_item(
            sheet, barcode_id, item_name, brand,
            category_id, category_name, size_label, condition,
            color, pattern, material, cost, price, photo_b64,
        )
        if ok and measurements_data:
            save_measurements(sheet, category_id, barcode_id, measurements_data)

    if ok:
        st.success("🎉 บันทึกสำเร็จ!")
        st.balloons()
        qr_bytes = generate_qr_bytes(barcode_id)
        if qr_bytes:
            render_qr_result(barcode_id, qr_bytes, item_name, brand, category_name, price)

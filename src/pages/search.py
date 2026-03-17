"""
pages/search.py — Search inventory with text query and status filter.
"""

import streamlit as st
from src.database.inventory import load_all_inventory, find_item_by_barcode, update_inventory_item
from src.components.ui_helpers import render_section, render_empty_state, render_divider
from src.config import SIZE_OPTIONS, CONDITION_OPTIONS
from datetime import datetime


def render(sheet):
    render_section("🔍 ค้นหาสินค้า")

    df = load_all_inventory(sheet)
    if df.empty:
        render_empty_state("🗄️", "ยังไม่มีข้อมูลสินค้าในระบบ")
        return

    col_q, col_s = st.columns([3, 1])
    with col_q:
        query = st.text_input(
            "ค้นหา",
            placeholder="🔎 พิมพ์ชื่อสินค้า แบรนด์ หรือรหัส...",
            label_visibility="collapsed",
        )
    with col_s:
        status_filter = st.selectbox(
            "สถานะ",
            ["ทั้งหมด", "คงเหลือ", "ขายแล้ว"],
            label_visibility="collapsed",
        )

    result = df.copy()

    if query:
        mask = (
            result["Item_Name"].str.contains(query, case=False, na=False) |
            result["Brand"].str.contains(query, case=False, na=False) |
            result["Barcode_ID"].str.contains(query, case=False, na=False)
        )
        result = result[mask]

    if status_filter == "คงเหลือ":
        result = result[result["Status"] == "Available"]
    elif status_filter == "ขายแล้ว":
        result = result[result["Status"] == "Sold"]

    # --- Aging stock highlights ---
    now = datetime.now()
    def format_item_name(row):
        name = str(row.get("Item_Name", ""))
        created_at = row.get("Created_At", "")
        if created_at and str(row.get("Status", "")) == "Available":
            try:
                dt = datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S")
                days = (now - dt).days
                if days >= 90:
                    return f"🚨 {name} (ค้างสต็อก {days} วัน)"
                elif days >= 30:
                    return f"⚠️ {name} (ค้างสต็อก {days} วัน)"
            except Exception:
                pass
        return name

    if not result.empty:
        result["Item_Name"] = result.apply(format_item_name, axis=1)

    label = f'พบ <strong>{len(result)}</strong> รายการ'
    if query:
        label += f' จากการค้นหา &quot;{query}&quot;'
    st.markdown(f'<div style="color:#666;font-size:.875rem;margin-bottom:10px;">{label}</div>', unsafe_allow_html=True)

    if result.empty:
        render_empty_state("🔍", "ไม่พบสินค้าที่ตรงกับการค้นหา")
        return

    if "Photo" in result.columns:
        # Create a new column with base64 data URI for Streamlit ImageColumn
        result["Image_Prev"] = result["Photo"].apply(
            lambda x: f"data:image/jpeg;base64,{x}" if str(x).strip() else None
        )
        show_cols = ["Image_Prev", "Barcode_ID", "Item_Name", "Brand", "Category_Name", "Size_Label", "Price", "Status"]
    else:
        show_cols = ["Barcode_ID", "Item_Name", "Brand", "Category_Name", "Size_Label", "Price", "Status"]
        
    disp_cols = [c for c in show_cols if c in result.columns]
    
    st.dataframe(
        result[disp_cols], 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Image_Prev": st.column_config.ImageColumn("รูปภาพ", help="รูปสินค้า"),
        }
    )

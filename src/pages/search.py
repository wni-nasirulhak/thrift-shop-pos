"""
pages/search.py — Search inventory with text query and status filter.
"""

import streamlit as st
from src.database.inventory import load_all_inventory
from src.components.ui_helpers import render_section, render_empty_state


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

    label = f'พบ <strong>{len(result)}</strong> รายการ'
    if query:
        label += f' จากการค้นหา &quot;{query}&quot;'
    st.markdown(f'<div style="color:#666;font-size:.875rem;margin-bottom:10px;">{label}</div>', unsafe_allow_html=True)

    if result.empty:
        render_empty_state("🔍", "ไม่พบสินค้าที่ตรงกับการค้นหา")
        return

    show_cols = ["Barcode_ID", "Item_Name", "Brand", "Category_Name", "Size_Label", "Price", "Status"]
    disp_cols = [c for c in show_cols if c in result.columns]
    st.dataframe(result[disp_cols], use_container_width=True, hide_index=True)

"""
app.py — Entry point for Thrift Shop POS.
Run with:  streamlit run app.py
"""

import streamlit as st
from src.config import APP_TITLE, APP_ICON, APP_VERSION
from src.components.styles import inject_css
from src.components.ui_helpers import render_header
from src.database.connection import connect_to_sheets
from src.database.catalog import load_categories, load_brands

import src.pages.dashboard       as page_dashboard
import src.pages.inventory_entry as page_inventory
import src.pages.pos             as page_pos
import src.pages.search          as page_search
import src.pages.edit_product    as page_edit

# ===== Page config (must be first Streamlit call) =====
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

# ===== Header =====
render_header(f"{APP_ICON} {APP_TITLE}", "ระบบจัดการร้านเสื้อผ้ามือสอง")

# ===== Connect =====
sheet = connect_to_sheets()
if sheet is None:
    st.stop()

categories_df = load_categories(sheet)
brands_df     = load_brands(sheet)

# ===== Navigation =====
MENU_ITEMS = [
    "🏠 Dashboard",
    "📦 รับของเข้าสต็อก",
    "🛒 จุดขายสินค้า",
    "🔍 ค้นหาสินค้า",
    "✏️ แก้ไขสินค้า",
]

# Sidebar (desktop)
with st.sidebar:
    st.markdown(
        '<div style="color:white;font-size:1.1rem;font-weight:700;padding:10px 0;">📋 เมนูหลัก</div>',
        unsafe_allow_html=True,
    )
    sidebar_menu = st.radio("เมนู", MENU_ITEMS, label_visibility="collapsed")
    st.markdown("---")
    if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown(
        f'<div style="color:#aaa;text-align:center;font-size:.75rem;margin-top:20px;">v{APP_VERSION}</div>',
        unsafe_allow_html=True,
    )

# Dropdown (mobile — stays in sync with sidebar)
mobile_menu = st.selectbox(
    "เมนู",
    MENU_ITEMS,
    index=MENU_ITEMS.index(sidebar_menu),
    label_visibility="collapsed",
)
menu = mobile_menu if mobile_menu != sidebar_menu else sidebar_menu

# ===== Route =====
if menu == "🏠 Dashboard":
    page_dashboard.render(sheet)

elif menu == "📦 รับของเข้าสต็อก":
    page_inventory.render(sheet, categories_df, brands_df)

elif menu == "🛒 จุดขายสินค้า":
    page_pos.render(sheet)

elif menu == "🔍 ค้นหาสินค้า":
    page_search.render(sheet)

elif menu == "✏️ แก้ไขสินค้า":
    page_edit.render(sheet)

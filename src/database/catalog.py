"""
database/catalog.py — Load Categories and Brands from Google Sheets.
These are reference data; changes are rare so TTL can be higher.
"""

import streamlit as st
import pandas as pd
from src.config import SHEET_CATEGORIES, SHEET_BRANDS, CACHE_TTL_CATALOG


@st.cache_data(ttl=CACHE_TTL_CATALOG)
def load_categories(_sheet) -> pd.DataFrame:
    """โหลด Categories sheet → DataFrame. (cached)"""
    try:
        ws = _sheet.worksheet(SHEET_CATEGORIES)
        data = ws.get_all_values()
        if len(data) <= 1:
            return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])
    except Exception as e:
        st.error(f"❌ โหลด Categories ไม่สำเร็จ: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL_CATALOG)
def load_brands(_sheet) -> pd.DataFrame:
    """โหลด Brands sheet → DataFrame. (cached)"""
    try:
        ws = _sheet.worksheet(SHEET_BRANDS)
        data = ws.get_all_values()
        if len(data) <= 1:
            return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])
    except Exception as e:
        st.error(f"❌ โหลด Brands ไม่สำเร็จ: {e}")
        return pd.DataFrame()


def get_active_categories(categories_df: pd.DataFrame) -> dict:
    """คืน dict {display_label: row} สำหรับ selectbox."""
    active = categories_df[categories_df["Active"] == "Yes"]
    return {
        f"{row['Category_Icon']} {row['Category_Name']}": row
        for _, row in active.iterrows()
    }


def get_active_brand_names(brands_df: pd.DataFrame) -> list[str]:
    """คืน list ชื่อแบรนด์ที่ active."""
    return brands_df[brands_df["Active"] == "Yes"]["Brand_Name"].tolist()


def get_brand_code(brands_df: pd.DataFrame, brand_name: str) -> str:
    """คืน Brand_Code จากชื่อแบรนด์."""
    row = brands_df[brands_df["Brand_Name"] == brand_name]
    if row.empty:
        return "UNK"
    return row.iloc[0]["Brand_Code"]

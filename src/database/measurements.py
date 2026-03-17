"""
database/measurements.py — Read/write measurement sheets.
Supports Shirts, Pants, Shoes. Add new categories in config.py.
"""

import streamlit as st
from datetime import datetime
from src.config import SHEET_MEASUREMENTS


def save_measurements(sheet, category_id: str, barcode_id: str, data: dict) -> bool:
    """บันทึกขนาดสินค้าลง measurement sheet ตาม category."""
    sheet_name = SHEET_MEASUREMENTS.get(category_id)
    if not sheet_name:
        return True  # Category ที่ไม่มี measurement — ถือว่าสำเร็จ

    try:
        ws = sheet.worksheet(sheet_name)
        row = _build_measurement_row(category_id, barcode_id, data)
        ws.append_row(row)
        return True
    except Exception as e:
        st.error(f"❌ บันทึกขนาดไม่สำเร็จ: {e}")
        return False


def load_measurements(sheet, category_id: str, barcode_id: str) -> dict:
    """โหลดขนาดสินค้าจาก measurement sheet. คืน dict หรือ {}."""
    sheet_name = SHEET_MEASUREMENTS.get(category_id)
    if not sheet_name:
        return {}

    try:
        ws = sheet.worksheet(sheet_name)
        records = ws.get_all_records()
        for rec in records:
            if str(rec.get("Barcode_ID", "")) == str(barcode_id):
                return rec
        return {}
    except Exception as e:
        st.error(f"❌ โหลดขนาดไม่สำเร็จ: {e}")
        return {}


# ===== Private helpers =====

def _build_measurement_row(category_id: str, barcode_id: str, data: dict) -> list:
    """แปลง dict ข้อมูลขนาดเป็น list row สำหรับ append_row."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if category_id == "CAT-SH":
        return [
            barcode_id,
            data.get("chest", 0),
            data.get("length", 0),
            data.get("sleeve", 0),
            data.get("shoulder", 0),
            data.get("collar_type", ""),
            data.get("fit", ""),
            now,
        ]

    if category_id == "CAT-PA":
        return [
            barcode_id,
            data.get("waist", 0),
            data.get("hip", 0),
            data.get("length", 0),
            data.get("inseam", 0),
            data.get("leg_opening", 0),
            data.get("rise", 0),
            data.get("thigh", 0),
            data.get("fit", ""),
            now,
        ]

    if category_id == "CAT-FW":
        return [
            barcode_id,
            data.get("size_us", ""),
            data.get("size_eu", ""),
            data.get("size_uk", ""),
            data.get("size_jp", ""),
            data.get("insole_length", 0),
            data.get("width", ""),
            data.get("heel_height", 0),
            data.get("condition_sole", ""),
            now,
        ]

    return [barcode_id, now]

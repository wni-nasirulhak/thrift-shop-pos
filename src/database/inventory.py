"""
database/inventory.py — CRUD operations for the Inventory sheet.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.config import SHEET_INVENTORY, INV_COL_STATUS, CACHE_TTL_INVENTORY


@st.cache_data(ttl=CACHE_TTL_INVENTORY)
def load_all_inventory(_sheet) -> pd.DataFrame:
    """โหลดสินค้าทั้งหมด → DataFrame. (cached)"""
    try:
        ws = _sheet.worksheet(SHEET_INVENTORY)
        data = ws.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ โหลด Inventory ไม่สำเร็จ: {e}")
        return pd.DataFrame()


def find_item_by_barcode(sheet, barcode_id: str) -> dict | None:
    """ค้นหาสินค้าจาก Barcode_ID. คืน dict หรือ None."""
    try:
        ws = sheet.worksheet(SHEET_INVENTORY)
        records = ws.get_all_records()
        for rec in records:
            if str(rec.get("Barcode_ID", "")) == str(barcode_id):
                return rec
        return None
    except Exception as e:
        st.error(f"❌ ค้นหาสินค้าไม่สำเร็จ: {e}")
        return None


def add_inventory_item(
    sheet,
    barcode_id: str,
    item_name: str,
    brand: str,
    category_id: str,
    category_name: str,
    size_label: str,
    condition: str,
    color: str,
    pattern: str,
    material: str,
    cost: float,
    price: float,
    photo_b64: str = "",
    added_by: str = "Admin",
) -> bool:
    """เพิ่มสินค้าใหม่เข้า Inventory sheet."""
    try:
        ws = sheet.worksheet(SHEET_INVENTORY)
        new_row = [
            barcode_id,
            item_name,
            brand,
            category_id,
            category_name,
            size_label,
            condition,
            color,
            pattern,
            material,
            float(cost),
            float(price),
            "Available",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            added_by,
            "",          # Consignment_Owner (future)
            "",          # Consignment_Rate (future)
            "",          # Notes
            photo_b64,   # Column S = Photo (Cloudinary URL JSON or legacy base64)
        ]
        ws.append_row(new_row)
        return True
    except Exception as e:
        st.error(f"❌ บันทึกสินค้าไม่สำเร็จ: {e}")
        return False


def update_item_status(sheet, barcode_id: str, status: str = "Sold") -> bool:
    """อัปเดตสถานะสินค้า (Available / Sold / Reserved)."""
    try:
        ws = sheet.worksheet(SHEET_INVENTORY)
        cell = ws.find(str(barcode_id))
        if cell:
            ws.update_cell(cell.row, INV_COL_STATUS, status)
            return True
        return False
    except Exception as e:
        st.error(f"❌ อัปเดตสถานะไม่สำเร็จ: {e}")
        return False


def update_inventory_item(
    sheet,
    barcode_id: str,
    item_name: str,
    brand: str,
    size_label: str,
    condition: str,
    color: str,
    pattern: str,
    material: str,
    cost: float,
    price: float,
    photo_b64: str = "",
) -> bool:
    """
    แก้ไขข้อมูลสินค้าที่มีอยู่แล้ว — ใช้ batch_update เพื่อความเร็วและน่าเชื่อถือ.
    Column layout (1-based):
      A=Barcode_ID, B=Item_Name, C=Brand, D=Cat_ID, E=Cat_Name,
      F=Size_Label, G=Condition, H=Color, I=Pattern, J=Material,
      K=Cost, L=Price, M=Status, N=Created_At, O=Added_By,
      P=Consignment_Owner, Q=Consignment_Rate, R=Notes, S=Photo
    """
    try:
        ws = sheet.worksheet(SHEET_INVENTORY)
        records = ws.get_all_records()

        for idx, rec in enumerate(records, start=2):  # row 1 = header
            if str(rec.get("Barcode_ID", "")) == str(barcode_id):
                cell_updates = [
                    {"range": f"B{idx}", "values": [[str(item_name)]]},
                    {"range": f"C{idx}", "values": [[str(brand)]]},
                    {"range": f"F{idx}", "values": [[str(size_label)]]},
                    {"range": f"G{idx}", "values": [[str(condition)]]},
                    {"range": f"H{idx}", "values": [[str(color)]]},
                    {"range": f"I{idx}", "values": [[str(pattern)]]},
                    {"range": f"J{idx}", "values": [[str(material)]]},
                    {"range": f"K{idx}", "values": [[float(cost)]]},
                    {"range": f"L{idx}", "values": [[float(price)]]},
                    {"range": f"S{idx}", "values": [[str(photo_b64)]]},  # Photo
                ]
                ws.batch_update(cell_updates)
                return True

        st.warning(f"⚠️ ไม่พบสินค้า {barcode_id}")
        return False
    except Exception as e:
        st.error(f"❌ แก้ไขสินค้าไม่สำเร็จ: {e}")
        return False

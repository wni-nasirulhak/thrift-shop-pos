"""
database/customers.py — Manage CRM data (Points, Customer Info)
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.config import SHEET_CUSTOMERS

def load_customer(sheet, phone: str) -> dict | None:
    """ค้นหาลูกค้าด้วยเบอร์โทรศัพท์"""
    try:
        ws = sheet.worksheet(SHEET_CUSTOMERS)
        records = ws.get_all_records()
        for rec in records:
            if str(rec.get("Phone_Number", "")) == str(phone):
                return rec
        return None
    except Exception as e:
        st.error(f"❌ โหลดข้อมูลลูกค้าไม่สำเร็จ: {e}")
        return None

def load_all_customers(sheet) -> list:
    """โหลดลูกค้าทั้งหมด (คืนค่าลิสต์ของ dict)"""
    try:
        ws = sheet.worksheet(SHEET_CUSTOMERS)
        return ws.get_all_records()
    except Exception as e:
        st.error(f"❌ โหลดข้อมูลลูกค้าไม่สำเร็จ: {e}")
        return []


def register_customer(sheet, phone: str, name: str) -> bool:
    """เพิ่มลูกค้าใหม่ในฐานข้อมูล"""
    try:
        ws = sheet.worksheet(SHEET_CUSTOMERS)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [
            str(phone),
            name,
            0,      # Points
            0.0,    # Total_Spent
            now,    # Last_Visit
            now,    # Created_At
        ]
        ws.append_row(new_row)
        return True
    except Exception as e:
        st.error(f"❌ ลงทะเบียนลูกค้าไม่สำเร็จ: {e}")
        return False


def update_customer_after_sale(sheet, phone: str, points_earned: int, points_used: int, spent_amount: float) -> bool:
    """อัปเดตแต้ม, ยอดใช้จ่ายรวม และวันที่มาใช้บริการล่าสุด"""
    try:
        ws = sheet.worksheet(SHEET_CUSTOMERS)
        records = ws.get_all_records()
        for idx, rec in enumerate(records, start=2): # +2 offsets header & 0-index
            if str(rec.get("Phone_Number", "")) == str(phone):
                current_points = int(rec.get("Points", 0) or 0)
                current_spent = float(rec.get("Total_Spent", 0) or 0)
                
                new_points = current_points - points_used + points_earned
                new_spent = current_spent + float(spent_amount)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Column check: 1=Phone, 2=Name, 3=Points, 4=Total_Spent, 5=Last_Visit
                updates = [
                    (idx, 3, new_points),
                    (idx, 4, new_spent),
                    (idx, 5, now),
                ]
                for row, col, val in updates:
                    ws.update_cell(row, col, val)
                return True
        return False
    except Exception as e:
        st.error(f"❌ อัปเดตข้อมูลลูกค้าไม่สำเร็จ: {e}")
        return False

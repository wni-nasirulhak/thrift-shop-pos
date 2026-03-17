"""
database/shipping.py — Manage shipping logs
"""

import streamlit as st
from datetime import datetime
from src.config import SHEET_SHIPPING
from src.database.inventory import update_item_status

def record_shipping(sheet, barcode_id: str, address: str, tracking_no: str, status: str = "Shipped") -> bool:
    """บันทึกการจัดส่งและอัปเดตสถานะเป็น Shipped"""
    try:
        ws = sheet.worksheet(SHEET_SHIPPING)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Headers: ["Sale_ID", "Barcode_ID", "Status", "Shipping_Address", "Tracking_No", "Updated_At"]
        # Fake Sale_ID since we might not have it strictly linked from POS here
        sale_id = f"SALE-{now.replace(' ', '').replace(':', '').replace('-', '')}"
        
        new_row = [
            sale_id,
            str(barcode_id),
            status,
            address,
            tracking_no,
            now
        ]
        ws.append_row(new_row)
        
        # อัปเดตสถานะสินค้า
        update_item_status(sheet, barcode_id, status)
        return True
    except Exception as e:
        st.error(f"❌ บันทึกการจัดส่งไม่สำเร็จ: {e}")
        return False

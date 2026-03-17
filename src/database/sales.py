"""
database/sales.py — Record sales transactions.
"""

import streamlit as st
from datetime import datetime
from src.config import SHEET_SALES
from src.database.inventory import update_item_status
from src.database.customers import update_customer_after_sale


def record_sale(
    sheet,
    barcode_id: str,
    original_price: float,
    discount_type: str,
    discount_value: float,
    final_price: float,
    payment_method: str,
    sold_by: str = "Admin",
    customer_phone: str = "",
    points_used: int = 0,
) -> bool:
    """บันทึกการขายลง Sales sheet และอัปเดตสถานะสินค้า."""
    try:
        sale_id = f"SALE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        receipt_id = f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        discount_amount = original_price - final_price

        ws = sheet.worksheet(SHEET_SALES)
        new_row = [
            sale_id,
            barcode_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            float(original_price),
            discount_type,
            float(discount_value) if discount_value else 0,
            float(discount_amount),
            float(final_price),
            payment_method,
            "",           # Customer_Note (future)
            sold_by,
            receipt_id,
            "",           # Refund_Status (future)
        ]
        ws.append_row(new_row)

        # อัปเดตสินค้าเป็น Sold
        update_item_status(sheet, barcode_id, "Sold")
        
        # ระบบ CRM (สะสมแต้ม)
        if customer_phone:
            points_earned = int(final_price // 100)
            update_customer_after_sale(sheet, customer_phone, points_earned, points_used, final_price)

        return True

    except Exception as e:
        st.error(f"❌ บันทึกการขายไม่สำเร็จ: {e}")
        return False


def load_sales_summary(sheet) -> dict:
    """โหลดสรุปยอดขาย สำหรับ Dashboard."""
    try:
        ws = sheet.worksheet(SHEET_SALES)
        records = ws.get_all_records()
        if not records:
            return {"total_sales": 0, "total_revenue": 0.0, "total_discount": 0.0}

        total_sales = len(records)
        total_revenue = sum(float(r.get("Final_Price", 0) or 0) for r in records)
        total_discount = sum(float(r.get("Discount_Amount", 0) or 0) for r in records)

        return {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "total_discount": total_discount,
        }
    except Exception as e:
        st.error(f"❌ โหลดข้อมูลการขายไม่สำเร็จ: {e}")
        return {"total_sales": 0, "total_revenue": 0.0, "total_discount": 0.0}

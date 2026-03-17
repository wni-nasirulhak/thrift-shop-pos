"""
pages/dashboard.py — Dashboard: inventory overview & key metrics.
"""

import streamlit as st
import pandas as pd
from src.database.inventory import load_all_inventory
from src.components.ui_helpers import (
    render_section, render_metric_grid, render_divider, render_empty_state
)
from datetime import datetime


def render(sheet):
    render_section("📊 Dashboard")

    df = load_all_inventory(sheet)

    if df.empty:
        render_empty_state("🗄️", "ยังไม่มีข้อมูลสินค้า<br>เริ่มต้นโดยเพิ่มสินค้าในเมนู 'รับของเข้าสต็อก'")
        return

    # ===== Key metrics =====
    total     = len(df)
    available = len(df[df["Status"] == "Available"])
    sold      = len(df[df["Status"] == "Sold"])

    sold_df = df[df["Status"] == "Sold"].copy()
    if not sold_df.empty:
        sold_df["Price"] = pd.to_numeric(sold_df["Price"], errors="coerce")
        sold_df["Cost"]  = pd.to_numeric(sold_df["Cost"],  errors="coerce")
        total_profit = (sold_df["Price"] - sold_df["Cost"]).sum()
    else:
        total_profit = 0.0

    render_metric_grid([
        {"value": total,              "label": "📦 สินค้าทั้งหมด",  "color_class": ""},
        {"value": available,          "label": "✅ คงเหลือ",         "color_class": "green"},
        {"value": sold,               "label": "💰 ขายแล้ว",        "color_class": "blue"},
        {"value": f"฿{total_profit:,.0f}", "label": "💵 กำไรรวม",   "color_class": "orange"},
    ])

    render_divider()
    render_section("📋 สินค้าคงเหลือ")

    avail_df = df[df["Status"] == "Available"]
    if avail_df.empty:
        render_empty_state("📭", "ไม่มีสินค้าคงเหลือในขณะนี้")
        return

    # --- Aging stock highlights ---
    now = datetime.now()
    def format_item_name(row):
        name = str(row.get("Item_Name", ""))
        created_at = row.get("Created_At", "")
        if created_at:
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

    avail_df["Item_Name"] = avail_df.apply(format_item_name, axis=1)

    if "Photo" in avail_df.columns:
        avail_df["Image_Prev"] = avail_df["Photo"].apply(
            lambda x: f"data:image/jpeg;base64,{x}" if str(x).strip() else None
        )
        show_cols = ["Image_Prev", "Barcode_ID", "Item_Name", "Brand", "Category_Name", "Size_Label", "Price"]
    else:
        show_cols = ["Barcode_ID", "Item_Name", "Brand", "Category_Name", "Size_Label", "Price"]

    disp_cols = [c for c in show_cols if c in avail_df.columns]
    
    st.dataframe(
        avail_df[disp_cols], 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Image_Prev": st.column_config.ImageColumn("รูปภาพ"),
        }
    )

# -*- coding: utf-8 -*-
"""
pages/batch_tools.py — Batch listing, filtering, and actions (print barcodes, labels).
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.database.inventory import load_all_inventory
from src.services.barcode import generate_qr_bytes

PAGE_SIZE = 50  # items per page

def render(sheet):
    st.markdown("## 📋 รายการสินค้าทั้งหมด")

    # ===== Load & Cache inventory =====
    with st.spinner("กำลังโหลดข้อมูล..."):
        df = load_all_inventory(sheet)

    if df.empty:
        st.info("ไม่พบสินค้าในระบบ")
        return

    # ===== Filters =====
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search_q = st.text_input("🔍 ค้นหาชื่อ / บาร์โค้ด", placeholder="พิมพ์ชื่อหรือรหัสสินค้า", label_visibility="collapsed")
    with col2:
        cats = ["ทั้งหมด"] + sorted(df["Category_Name"].dropna().unique().tolist())
        cat_filter = st.selectbox("หมวดหมู่", cats, label_visibility="collapsed")
    with col3:
        statuses = ["ทั้งหมด"] + sorted(df["Status"].dropna().unique().tolist())
        status_filter = st.selectbox("สถานะ", statuses, label_visibility="collapsed")
    with col4:
        if st.button("🔄 รีเฟรช", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # ===== Apply Filters =====
    filtered = df.copy()
    if search_q:
        mask = (
            filtered["Item_Name"].astype(str).str.contains(search_q, case=False, na=False) |
            filtered["Barcode_ID"].astype(str).str.contains(search_q, case=False, na=False)
        )
        filtered = filtered[mask]
    if cat_filter != "ทั้งหมด":
        filtered = filtered[filtered["Category_Name"] == cat_filter]
    if status_filter != "ทั้งหมด":
        filtered = filtered[filtered["Status"] == status_filter]
    else:
        # Default: show Available items first
        status_order = {"Available": 0, "Reserved": 1, "Sold": 2, "Shipped": 3}
        filtered["_order"] = filtered["Status"].map(status_order).fillna(9)
        filtered = filtered.sort_values("_order").drop(columns=["_order"])

    # ===== Pagination =====
    total_items = len(filtered)
    total_pages = max(1, (total_items + PAGE_SIZE - 1) // PAGE_SIZE)

    page_col, info_col = st.columns([2, 4])
    with page_col:
        current_page = st.number_input(
            "หน้า", min_value=1, max_value=total_pages, value=1, step=1,
            label_visibility="collapsed"
        )
    with info_col:
        st.caption(f"แสดง {min(PAGE_SIZE, total_items)} จาก {total_items} รายการ | หน้า {current_page}/{total_pages}")

    start = (current_page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    page_df = filtered.iloc[start:end].reset_index(drop=True)

    # ===== Selectable Table =====
    st.markdown("---")
    
    # Add a Select column for checkboxes
    display_cols = ["Barcode_ID", "Item_Name", "Brand", "Category_Name", "Size_Label", "Status", "Price"]
    display_cols = [c for c in display_cols if c in page_df.columns]
    
    show_df = page_df[display_cols].copy()
    show_df.insert(0, "เลือก", False)

    # Add aging indicator
    if "Created_At" in page_df.columns:
        today = datetime.now()
        def age_badge(created):
            try:
                age = (today - datetime.strptime(str(created), "%Y-%m-%d %H:%M:%S")).days
                if age > 90: return f"🚨 {age}d"
                if age > 30: return f"⚠️ {age}d"
                return f"{age}d"
            except:
                return ""
        show_df["อายุ (วัน)"] = page_df["Created_At"].apply(age_badge)

    edited = st.data_editor(
        show_df,
        hide_index=True,
        use_container_width=True,
        key="batch_table",
        column_config={
            "เลือก": st.column_config.CheckboxColumn("เลือก", help="ติ๊กเลือกรายการ"),
            "Price": st.column_config.NumberColumn("ราคา (฿)", format="฿%.0f"),
        }
    )

    # ===== Selected items =====
    selected_mask = edited["เลือก"] == True
    selected_rows = page_df[selected_mask.values]
    selected_count = len(selected_rows)

    # ===== Batch Action Buttons =====
    st.markdown(f"**เลือกแล้ว {selected_count} รายการ**")
    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("🏷️ พิมพ์บาร์โค้ด / QR Code", use_container_width=True, disabled=selected_count == 0):
            _render_barcode_print(selected_rows)

    with action_col2:
        if st.button("📦 พิมพ์ใบปะหน้าพัสดุ", use_container_width=True, disabled=selected_count == 0):
            _render_shipping_labels(selected_rows, sheet)

    with action_col3:
        if st.button("📊 Export รายการ (CSV)", use_container_width=True, disabled=selected_count == 0):
            csv_data = selected_rows[display_cols].to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                "⬇️ ดาวน์โหลด CSV",
                data=csv_data,
                file_name=f"inventory_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )


def _render_barcode_print(selected_rows: pd.DataFrame):
    """Renders a printable grid of QR codes for selected items."""
    st.markdown("---")
    st.markdown("### 🏷️ พิมพ์บาร์โค้ด/QR Code")
    st.caption("กด **Ctrl+P** หรือ **Command+P** เพื่อพิมพ์หน้านี้")

    cols = st.columns(4)
    for idx, (_, row) in enumerate(selected_rows.iterrows()):
        barcode_id = str(row.get("Barcode_ID", ""))
        item_name = str(row.get("Item_Name", ""))[:24]
        price = row.get("Price", 0)
        
        try:
            from src.services.barcode import generate_qr_bytes
            qr_bytes = generate_qr_bytes(barcode_id)
        except Exception:
            qr_bytes = None

        with cols[idx % 4]:
            st.markdown(f"""
            <div style="border:1px solid #ddd;border-radius:8px;padding:8px;text-align:center;margin-bottom:8px;">
                <div style="font-size:0.65rem;color:#888;margin-bottom:4px;">{barcode_id}</div>
                <div style="font-weight:600;font-size:0.75rem;margin-bottom:4px;">{item_name}</div>
                <div style="color:#4f46e5;font-weight:700;">฿{float(price):,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            if qr_bytes:
                st.image(qr_bytes, use_container_width=True)


def _render_shipping_labels(selected_rows: pd.DataFrame, sheet):
    """Renders simple shipping labels for selected items."""
    from src.config import SHEET_SHIPPING
    
    # Try to load shipping data
    shipping_map = {}
    try:
        ws = sheet.worksheet(SHEET_SHIPPING)
        shipping_records = ws.get_all_records()
        for rec in shipping_records:
            bid = str(rec.get("Barcode_ID", ""))
            if bid:
                shipping_map[bid] = rec
    except Exception:
        pass

    st.markdown("---")
    st.markdown("### 📦 พิมพ์ใบปะหน้าพัสดุ")
    st.caption("กด **Ctrl+P** หรือ **Command+P** เพื่อพิมพ์หน้านี้")

    for _, row in selected_rows.iterrows():
        bid = str(row.get("Barcode_ID", ""))
        shipping_info = shipping_map.get(bid, {})
        address = shipping_info.get("Shipping_Address", "(ไม่มีที่อยู่ในระบบ)")
        tracking = shipping_info.get("Tracking_No", "-")
        status = shipping_info.get("Status", row.get("Status", ""))

        st.markdown(f"""
        <div style="border:2px solid #1e293b;border-radius:12px;padding:20px;margin-bottom:16px;font-family:sans-serif;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div style="font-size:0.75rem;color:#888;margin-bottom:4px;">จาก: ร้าน Thrift Shop</div>
                    <div style="font-size:1rem;font-weight:700;margin-bottom:12px;">ถึง: {address}</div>
                    <div style="font-size:0.8rem;color:#475569;">สินค้า: <strong>{row.get("Item_Name","")}</strong></div>
                    <div style="font-size:0.8rem;color:#475569;">รหัส: {bid}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.7rem;color:#888;">เลขติดตาม</div>
                    <div style="font-size:1.1rem;font-weight:800;color:#4f46e5;letter-spacing:2px;">{tracking}</div>
                    <div style="margin-top:8px;background:#f1f5f9;border-radius:6px;padding:4px 10px;font-size:0.75rem;">สถานะ: {status}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

"""
components/ui_helpers.py — Reusable UI widget builders.
Keep Streamlit rendering calls here so pages stay clean.
"""

import streamlit as st


def render_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="app-header">
        <h1>{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
def render_section(title: str, step: int | None = None):
    badge = f'<div class="step-badge">{step}</div>' if step else ""
    st.markdown(f"""
    <div class="section-header">
        {badge}
        <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)


def render_divider():
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


def render_metric_grid(metrics: list[dict]):
    """
    metrics: [{"value": ..., "label": ..., "color_class": "green|blue|orange|"}]
    """
    cards_html = ""
    for m in metrics:
        cls = m.get("color_class", "")
        cards_html += f"""
        <div class="metric-card {cls}">
            <div class="metric-value">{m["value"]}</div>
            <div class="metric-label">{m["label"]}</div>
        </div>"""
    st.markdown(f'<div class="metric-grid">{cards_html}</div>', unsafe_allow_html=True)


def render_barcode_preview(barcode_id: str):
    st.markdown(
        f'<div class="barcode-box">🏷️ บาร์โค้ด: {barcode_id}</div>',
        unsafe_allow_html=True,
    )


def render_qr_result(barcode_id: str, qr_bytes: bytes, item_name: str, brand: str, category: str, price: float):
    """แสดง QR Code + ข้อมูลสินค้า + ปุ่มดาวน์โหลด."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="qr-container">', unsafe_allow_html=True)
        st.image(qr_bytes, caption="QR Code", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="qr-info">
            <p>🏷️ <strong>รหัส:</strong> {barcode_id}</p>
            <p>📝 <strong>สินค้า:</strong> {item_name}</p>
            <p>🏷️ <strong>แบรนด์:</strong> {brand}</p>
            <p>📂 <strong>หมวด:</strong> {category}</p>
            <p>💰 <strong>ราคา:</strong> ฿{price:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "💾 ดาวน์โหลด QR Code",
            data=qr_bytes,
            file_name=f"{barcode_id}.png",
            mime="image/png",
            use_container_width=True,
        )


def render_item_card(item: dict):
    """แสดง card ข้อมูลสินค้า (ใช้ใน POS)."""
    st.markdown(f"""
    <div class="item-card">
        <h4>📦 {item.get('Item_Name', '')}</h4>
        <div class="item-detail">
            <span class="detail-label">รหัส</span>
            <span class="detail-value">{item.get('Barcode_ID', '')}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">แบรนด์</span>
            <span class="detail-value">{item.get('Brand', 'N/A')}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">หมวด</span>
            <span class="detail-value">{item.get('Category_Name', 'N/A')}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">ไซส์</span>
            <span class="detail-value">{item.get('Size_Label', 'N/A')}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">สภาพ</span>
            <span class="detail-value">{item.get('Condition', 'N/A')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_price_box(price: float, cost: float):
    profit = price - cost
    st.markdown(f"""
    <div class="price-box">
        <div class="price-label">ราคาขาย</div>
        <div class="price-main">฿{price:,.0f}</div>
        <div class="price-sub">ต้นทุน ฿{cost:,.0f} | กำไร ฿{profit:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)


def render_receipt(item_name: str, price: float, discount_amount: float, final_price: float, payment: str, timestamp: str):
    discount_html = ""
    if discount_amount > 0:
        discount_html = f"""
        <div class="receipt-row">
            <span>ส่วนลด</span><span>-฿{discount_amount:,.2f}</span>
        </div>"""
    st.markdown(f"""
    <div class="success-receipt">
        <h3>🧾 ใบเสร็จรับเงิน</h3>
        <div class="receipt-row"><span>สินค้า</span><span>{item_name}</span></div>
        <div class="receipt-row"><span>ราคา</span><span>฿{price:,.2f}</span></div>
        {discount_html}
        <div class="receipt-row"><span>ชำระด้วย</span><span>{payment}</span></div>
        <div class="receipt-row total"><span>💰 ยอดชำระ</span><span>฿{final_price:,.2f}</span></div>
        <div style="text-align:center;margin-top:12px;opacity:.8;font-size:.8rem;">{timestamp}</div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon: str, message: str):
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">{icon}</div>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_profit_hint(cost: float, price: float):
    """แสดงกำไรประมาณการใต้ช่องราคา."""
    if cost > 0 and price > 0:
        profit = price - cost
        pct = profit / cost * 100
        ok = profit >= 0
        bg = "#d4edda" if ok else "#f8d7da"
        fg = "#155724" if ok else "#721c24"
        st.markdown(
            f'<div style="background:{bg};color:{fg};padding:10px 16px;'
            f'border-radius:10px;font-size:.875rem;font-weight:600;">'
            f'💡 กำไรโดยประมาณ: ฿{profit:,.0f} ({pct:+.0f}%)</div>',
            unsafe_allow_html=True,
        )

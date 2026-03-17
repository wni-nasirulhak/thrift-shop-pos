# -*- coding: utf-8 -*-
"""
components/ui_helpers.py — Reusable UI widget builders.
Keep Streamlit rendering calls here so pages stay clean.
"""

import streamlit as st


def render_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="
        display:flex;align-items:center;gap:12px;
        padding:10px 16px;margin-bottom:8px;
        background:linear-gradient(135deg,#4f46e5,#7c3aed);
        border-radius:12px;
    ">
        <span style="font-size:1.4rem;">👕</span>
        <div style="flex:1;">
            <span style="color:white;font-weight:700;font-size:1rem;letter-spacing:.3px;">{title}</span>
            {f'<span style="color:#c4b5fd;font-size:.75rem;margin-left:8px;">{subtitle}</span>' if subtitle else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_section(title: str, step: int | None = None):
    badge = '<div class="step-badge">{}</div>'.format(step) if step else ""
    st.markdown("""
    <div class="section-header">
        {badge}
        <h3>{title}</h3>
    </div>
    """.format(badge=badge, title=title), unsafe_allow_html=True)


def render_divider():
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


def render_metric_grid(metrics: list[dict]):
    """
    metrics: [{"value": ..., "label": ..., "color_class": "green|blue|orange|"}]
    """
    cards_html = ""
    for m in metrics:
        cls = m.get("color_class", "")
        cards_html += """
        <div class="metric-card {cls}">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""".format(cls=cls, val=m["value"], label=m["label"])
    st.markdown('<div class="metric-grid">{}</div>'.format(cards_html), unsafe_allow_html=True)


def render_barcode_preview(barcode_id: str):
    st.markdown(
        '<div class="barcode-box">&#x1f3f7; บาร์โค้ด: {}</div>'.format(barcode_id),
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
        st.markdown("""
        <div class="qr-info">
            <p><strong>รหัส:</strong> {barcode_id}</p>
            <p><strong>สินค้า:</strong> {item_name}</p>
            <p><strong>แบรนด์:</strong> {brand}</p>
            <p><strong>หมวด:</strong> {category}</p>
            <p><strong>ราคา:</strong> &#3647;{price:,.2f}</p>
        </div>
        """.format(
            barcode_id=barcode_id,
            item_name=item_name,
            brand=brand,
            category=category,
            price=price
        ), unsafe_allow_html=True)
        st.download_button(
            "💾 ดาวน์โหลด QR Code",
            data=qr_bytes,
            file_name=f"{barcode_id}.png",
            mime="image/png",
            use_container_width=True,
        )


def render_item_card(item: dict):
    """แสดง card ข้อมูลสินค้า (ใช้ใน POS)."""
    st.markdown("""
    <div class="item-card">
        <h4>&#x1f4e6; {item_name}</h4>
        <div class="item-detail">
            <span class="detail-label">รหัส</span>
            <span class="detail-value">{barcode}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">แบรนด์</span>
            <span class="detail-value">{brand}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">หมวด</span>
            <span class="detail-value">{category}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">ไซส์</span>
            <span class="detail-value">{size}</span>
        </div>
        <div class="item-detail">
            <span class="detail-label">สภาพ</span>
            <span class="detail-value">{condition}</span>
        </div>
    </div>
    """.format(
        item_name=item.get('Item_Name', ''),
        barcode=item.get('Barcode_ID', ''),
        brand=item.get('Brand', 'N/A'),
        category=item.get('Category_Name', 'N/A'),
        size=item.get('Size_Label', 'N/A'),
        condition=item.get('Condition', 'N/A')
    ), unsafe_allow_html=True)


def render_price_box(price: float, cost: float):
    profit = price - cost
    st.markdown("""
    <div class="price-box">
        <div class="price-label">ราคาขาย</div>
        <div class="price-main">&#3647;{price:,.0f}</div>
        <div class="price-sub">ต้นทุน &#3647;{cost:,.0f} | กำไร &#3647;{profit:,.0f}</div>
    </div>
    """.format(price=price, cost=cost, profit=profit), unsafe_allow_html=True)


def render_receipt(item_name: str, price: float, discount_amount: float, final_price: float, payment: str, timestamp: str):
    discount_html = ""
    if discount_amount > 0:
        discount_html = """
        <div class="receipt-row">
            <span>ส่วนลด</span><span>-&#3647;{discount_amount:,.2f}</span>
        </div>""".format(discount_amount=discount_amount)
    st.markdown("""
    <div class="success-receipt">
        <h3>&#x1f9fe; ใบเสร็จรับเงิน</h3>
        <div class="receipt-row"><span>สินค้า</span><span>{item_name}</span></div>
        <div class="receipt-row"><span>ราคา</span><span>&#3647;{price:,.2f}</span></div>
        {discount_html}
        <div class="receipt-row"><span>ชำระด้วย</span><span>{payment}</span></div>
        <div class="receipt-row total"><span>&#x1f4b0; ยอดชำระ</span><span>&#3647;{final_price:,.2f}</span></div>
        <div style="text-align:center;margin-top:12px;opacity:.8;font-size:.8rem;">{timestamp}</div>
    </div>
    """.format(
        item_name=item_name,
        price=price,
        discount_html=discount_html,
        payment=payment,
        final_price=final_price,
        timestamp=timestamp
    ), unsafe_allow_html=True)


def render_empty_state(icon: str, message: str):
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">{icon}</div>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_profit_hint(cost: float, price: float):
    # แสดงกำไรประมาณการใต้ช่องราคา
    if cost > 0 and price > 0:
        profit = price - cost
        pct = profit / cost * 100
        ok = profit >= 0
        bg = "#d4edda" if ok else "#f8d7da"
        fg = "#155724" if ok else "#721c24"
        st.markdown(
            '<div style="background:{bg};color:{fg};padding:10px 16px;'
            'border-radius:10px;font-size:.875rem;font-weight:600;">'
            '&#x1f4a1; กำไรโดยประมาณ: &#3647;{profit:,.0f} ({pct:+.0f}%)</div>'.format(
                bg=bg, fg=fg, profit=profit, pct=pct
            ),
            unsafe_allow_html=True,
        )

"""
components/styles.py — Global CSS injected once at app startup.
Edit this file to change the visual design without touching page logic.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
    /* ===== CSS Variables ===== */
    :root {
        --primary:      #6C63FF;
        --primary-dark: #5A52D5;
        --secondary:    #FF6584;
        --success:      #43E97B;
        --info:         #4FACFE;
        --warning:      #F7B731;
        --danger:       #e74c3c;
        --bg-light:     #F8F9FE;
        --text-dark:    #1a1a2e;
        --text-muted:   #888;
        --card-shadow:  0 4px 20px rgba(108, 99, 255, 0.12);
        --radius:       16px;
        --radius-sm:    10px;
    }

    /* ===== Layout ===== */
    .main .block-container {
        padding: 1rem 1rem 3rem 1rem;
        max-width: 960px;
    }
    @media (max-width: 768px) {
        .main .block-container { padding: 0.5rem 0.5rem 4rem 0.5rem; }
    }

    /* ===== App Header ===== */
    .app-header {
        background: linear-gradient(135deg, #6C63FF 0%, #a855f7 100%);
        padding: 18px 24px;
        border-radius: var(--radius);
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: var(--card-shadow);
    }
    .app-header h1 { margin: 0; font-size: clamp(1.4rem, 4vw, 2rem); font-weight: 800; }
    .app-header p  { margin: 4px 0 0 0; opacity: .88; font-size: clamp(.75rem, 2.5vw, .9rem); }

    /* ===== Metric Cards ===== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }
    @media (min-width: 640px) { .metric-grid { grid-template-columns: repeat(4, 1fr); } }

    .metric-card {
        background: white;
        border-radius: var(--radius);
        padding: 16px;
        text-align: center;
        box-shadow: var(--card-shadow);
        border-top: 4px solid var(--primary);
        transition: transform .2s, box-shadow .2s;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(108,99,255,.2); }
    .metric-card.green  { border-top-color: var(--success); }
    .metric-card.blue   { border-top-color: var(--info); }
    .metric-card.orange { border-top-color: var(--warning); }
    .metric-value { font-size: clamp(1.5rem, 5vw, 2.2rem); font-weight: 800; color: var(--text-dark); line-height: 1.1; }
    .metric-label { font-size: .78rem; color: var(--text-muted); margin-top: 4px; font-weight: 500; }

    /* ===== Section Headers ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 20px 0 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid #f0f0f8;
    }
    .section-header h3 { margin: 0; font-size: 1.05rem; font-weight: 700; color: var(--text-dark); }
    .step-badge {
        background: var(--primary); color: white;
        border-radius: 50%; width: 28px; height: 28px;
        display: flex; align-items: center; justify-content: center;
        font-size: .8rem; font-weight: 800; flex-shrink: 0;
    }

    /* ===== Cards ===== */
    .info-card {
        background: white;
        border-radius: var(--radius);
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,.06);
        border: 1px solid #f0f0f8;
        margin: 12px 0;
    }
    .measurement-card {
        background: linear-gradient(135deg, #f0f8ff 0%, #e8f4fd 100%);
        border-radius: var(--radius);
        padding: 20px;
        border-left: 4px solid var(--info);
        margin: 12px 0;
    }
    .item-card {
        background: white;
        border-radius: var(--radius);
        padding: 18px;
        box-shadow: var(--card-shadow);
        border-left: 4px solid var(--success);
    }
    .item-card h4 { margin: 0 0 12px; color: var(--text-dark); font-size: 1rem; }
    .item-detail {
        display: flex; gap: 8px;
        padding: 5px 0;
        border-bottom: 1px solid #f5f5f5;
        font-size: .875rem; align-items: center;
    }
    .item-detail:last-child { border-bottom: none; }
    .detail-label { color: var(--text-muted); min-width: 80px; font-size: .8rem; }
    .detail-value { font-weight: 600; color: var(--text-dark); }

    /* ===== Barcode Box ===== */
    .barcode-box {
        font-family: 'Courier New', monospace;
        font-size: clamp(.9rem, 3vw, 1.2rem);
        font-weight: 700; color: var(--primary);
        text-align: center; padding: 14px 20px;
        background: #f8f7ff;
        border-radius: var(--radius-sm);
        border: 2px dashed var(--primary);
        margin: 12px 0; letter-spacing: 2px;
    }

    /* ===== QR Container ===== */
    .qr-container {
        background: white; border-radius: var(--radius);
        padding: 20px; box-shadow: var(--card-shadow);
        text-align: center; border: 2px solid #f0f0f8;
    }
    .qr-info {
        background: var(--bg-light);
        border-radius: var(--radius-sm); padding: 16px;
    }
    .qr-info p { margin: 4px 0; font-size: .875rem; }

    /* ===== Price Box ===== */
    .price-box {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        border-radius: var(--radius); padding: 16px 20px;
        color: white; text-align: center;
    }
    .price-main  { font-size: clamp(1.6rem, 6vw, 2.5rem); font-weight: 800; }
    .price-label { font-size: .8rem; opacity: .9; }
    .price-sub   { font-size: .85rem; opacity: .85; margin-top: 4px; }

    /* ===== Receipt ===== */
    .success-receipt {
        background: linear-gradient(135deg, #6C63FF 0%, #a855f7 100%);
        border-radius: var(--radius); padding: 24px; color: white; margin: 16px 0;
    }
    .success-receipt h3 { text-align: center; margin: 0 0 16px; font-size: 1.1rem; }
    .receipt-row {
        display: flex; justify-content: space-between;
        padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,.2);
        font-size: .9rem;
    }
    .receipt-row.total {
        font-size: 1.1rem; font-weight: 800;
        border-bottom: none; margin-top: 8px;
    }

    /* ===== Discount Badge ===== */
    .discount-badge {
        background: #fff3cd; color: #856404;
        border-radius: 8px; padding: 10px 16px;
        font-weight: 600; text-align: center;
        margin: 8px 0; border: 1px solid #ffc107; font-size: .9rem;
    }

    /* ===== Buttons ===== */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        min-height: 48px !important;
        font-size: .95rem !important;
        transition: all .2s !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C63FF, #a855f7) !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(108,99,255,.4) !important;
    }

    /* ===== Inputs ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div { border-radius: 10px !important; min-height: 44px !important; }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] { background: #1a1a2e; }
    section[data-testid="stSidebar"] .stRadio label { color: white !important; }

    /* ===== Misc ===== */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e0e0f0, transparent);
        margin: 20px 0;
    }
    .empty-state { text-align: center; padding: 40px 20px; color: #aaa; }
    .empty-state .icon { font-size: 3rem; margin-bottom: 12px; }
    .empty-state p { font-size: .9rem; }
</style>
"""


def inject_css():
    """Call once in app.py to inject global styles."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

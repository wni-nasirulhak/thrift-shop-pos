"""
components/styles.py — Global CSS injected once at app startup.
Edit this file to change the visual design without touching page logic.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Prompt:wght@300;400;500;600;700&display=swap');

    /* ===== CSS Variables ===== */
    :root {
        --primary:      #6C63FF;
        --primary-dark: #5A52D5;
        --secondary:    #FF6584;
        --success:      #10b981;
        --info:         #3b82f6;
        --warning:      #f59e0b;
        --danger:       #ef4444;
        --bg-light:     #f8fafc;
        --text-dark:    #0f172a;
        --text-muted:   #64748b;
        --card-shadow:  0 10px 25px -5px rgba(108, 99, 255, 0.1), 0 8px 10px -6px rgba(108, 99, 255, 0.1);
        --radius:       20px;
        --radius-sm:    12px;
        --font-main:    'Prompt', sans-serif;
        --font-heading: 'Kanit', sans-serif;
    }

    /* ===== Typography & Layout ===== */
    html, body, [class*="css"] {
        font-family: var(--font-main) !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading) !important;
        letter-spacing: -0.02em;
    }
    .main .block-container {
        padding: 1.5rem 1rem 4rem 1rem;
        max-width: 1000px;
        background-color: var(--bg-light);
    }
    @media (max-width: 768px) {
        .main .block-container { padding: 1rem 0.5rem 5rem 0.5rem; }
    }

    /* ===== App Header (Glassmorphism) ===== */
    .app-header {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.9) 0%, rgba(168, 85, 247, 0.9) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 24px 32px;
        border-radius: var(--radius);
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .app-header h1 { margin: 0; font-size: clamp(1.8rem, 5vw, 2.5rem); font-weight: 800; text-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .app-header p  { margin: 8px 0 0 0; opacity: .9; font-size: clamp(.85rem, 2.5vw, 1rem); font-weight: 300; }

    /* ===== Metric Cards ===== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 30px;
    }
    @media (min-width: 640px) { .metric-grid { grid-template-columns: repeat(4, 1fr); } }

    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: var(--radius);
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-top: 5px solid var(--primary);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover { 
        transform: translateY(-5px) scale(1.02); 
        box-shadow: var(--card-shadow); 
    }
    .metric-card.green  { border-top-color: var(--success); }
    .metric-card.blue   { border-top-color: var(--info); }
    .metric-card.orange { border-top-color: var(--warning); }
    .metric-value { font-size: clamp(1.8rem, 5vw, 2.5rem); font-family: var(--font-heading); font-weight: 700; color: var(--text-dark); line-height: 1.1; }
    .metric-label { font-size: .85rem; color: var(--text-muted); margin-top: 8px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

    /* ===== Section Headers ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 30px 0 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(108, 99, 255, 0.1);
    }
    .section-header h3 { margin: 0; font-size: 1.25rem; font-weight: 600; color: var(--text-dark); }
    .step-badge {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border-radius: 50%; width: 32px; height: 32px;
        display: flex; align-items: center; justify-content: center;
        font-size: .9rem; font-weight: 700; flex-shrink: 0;
        box-shadow: 0 4px 10px rgba(108, 99, 255, 0.3);
    }

    /* ===== Cards ===== */
    .info-card {
        background: white;
        border-radius: var(--radius);
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin: 16px 0;
        transition: box-shadow 0.3s ease;
    }
    .info-card:hover { box-shadow: var(--card-shadow); }
    
    .measurement-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: var(--radius);
        padding: 24px;
        border-left: 5px solid var(--info);
        margin: 16px 0;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.05);
    }
    
    .item-card {
        background: white;
        border-radius: var(--radius);
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 5px solid var(--success);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .item-card:hover { transform: translateY(-3px); box-shadow: var(--card-shadow); }
    .item-card h4 { margin: 0 0 16px; color: var(--text-dark); font-size: 1.1rem; font-weight: 600; }
    .item-detail {
        display: flex; gap: 12px;
        padding: 8px 0;
        border-bottom: 1px dashed #e2e8f0;
        font-size: .95rem; align-items: center;
    }
    .item-detail:last-child { border-bottom: none; }
    .detail-label { color: var(--text-muted); min-width: 85px; font-size: .85rem; font-weight: 500; }
    .detail-value { font-weight: 600; color: var(--text-dark); }

    /* ===== QR / Barcode Box ===== */
    .barcode-box {
        font-family: 'Courier New', Courier, monospace;
        font-size: clamp(1rem, 3vw, 1.3rem);
        font-weight: 700; color: var(--primary-dark);
        text-align: center; padding: 18px 24px;
        background: #f5f3ff;
        border-radius: var(--radius-sm);
        border: 2px dashed rgba(108, 99, 255, 0.4);
        margin: 16px 0; letter-spacing: 3px;
    }

    /* ===== Price Box ===== */
    .price-box {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        border-radius: var(--radius); padding: 20px 24px;
        color: white; text-align: center;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
    }
    .price-main  { font-size: clamp(1.8rem, 6vw, 2.8rem); font-family: var(--font-heading); font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .price-label { font-size: .9rem; opacity: .9; font-weight: 500; letter-spacing: 0.05em; }
    .price-sub   { font-size: .9rem; opacity: .9; margin-top: 8px; background: rgba(0,0,0,0.1); padding: 4px 12px; border-radius: 20px; display: inline-block; }

    /* ===== Success Receipt ===== */
    .success-receipt {
        background: linear-gradient(135deg, #6C63FF 0%, #8b5cf6 100%);
        border-radius: var(--radius); padding: 28px; color: white; margin: 20px 0;
        box-shadow: 0 10px 25px -5px rgba(108, 99, 255, 0.4);
        position: relative; overflow: hidden;
    }
    .success-receipt::before {
        content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    }
    .success-receipt h3 { text-align: center; margin: 0 0 20px; font-size: 1.25rem; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 12px; }
    .receipt-row {
        display: flex; justify-content: space-between;
        padding: 8px 0; border-bottom: 1px dashed rgba(255,255,255,.2);
        font-size: .95rem; position: relative; z-index: 1;
    }
    .receipt-row.total {
        font-size: 1.25rem; font-weight: 700;
        border-bottom: none; margin-top: 12px; padding-top: 12px; border-top: 2px solid rgba(255,255,255,0.4);
    }

    /* ===== Inputs & Selects ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div { 
        border-radius: var(--radius-sm) !important; 
        min-height: 48px !important; 
        font-family: var(--font-main) !important;
        border-color: #cbd5e1 !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
    }

    /* ===== Buttons ===== */
    .stButton > button {
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-heading) !important;
        font-weight: 600 !important;
        min-height: 52px !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid #e2e8f0 !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        border: none !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px -5px rgba(108, 99, 255, 0.5) !important;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] { 
        background: #312e81;   /* indigo-900 — lighter purple instead of near-black */
        border-right: 1px solid #3730a3;
    }
    section[data-testid="stSidebar"] .stRadio label { 
        color: #e0e7ff !important;   /* indigo-100 */ 
        font-weight: 500 !important;
        padding: 4px 0 !important;
    }
    section[data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-color: rgba(255,255,255,0.15) !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.2) !important;
    }

    /* ===== Misc ===== */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(108, 99, 255, 0.2), transparent);
        margin: 30px 0;
    }
    .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); background: white; border-radius: var(--radius); border: 1px dashed #cbd5e1; }
    .empty-state .icon { font-size: 3.5rem; margin-bottom: 16px; opacity: 0.8; }
    .empty-state p { font-size: 1rem; font-weight: 500; }
</style>
"""


def inject_css():
    """Call once in app.py to inject global styles."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

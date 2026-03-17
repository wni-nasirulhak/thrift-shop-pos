"""
database/connection.py — Google Sheets connection & caching.
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def connect_to_sheets():
    """เชื่อมต่อ Google Sheets ด้วย Service Account. Cache ตลอด session."""
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES,
        )
        client = gspread.authorize(credentials)
        sheet = client.open(st.secrets["sheet_name"])
        return sheet
    except Exception as e:
        st.error(f"❌ เชื่อมต่อ Google Sheets ไม่สำเร็จ: {e}")
        st.info("💡 ตรวจสอบไฟล์ .streamlit/secrets.toml และสิทธิ์ Service Account")
        return None

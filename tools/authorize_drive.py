"""
tools/authorize_drive.py — One-time Google Drive OAuth 2.0 setup.
Run once from project root:  python tools/authorize_drive.py

Saves token.pickle to project root for use by DriveImageService.
Requires credentials.json (downloaded from Google Cloud Console).
"""

import os
import pickle
import sys

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.pickle"


def authorize():
    # Must be run from project root
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ ไม่พบ {CREDENTIALS_FILE}")
        print("   ดาวน์โหลดจาก Google Cloud Console → APIs & Services → Credentials")
        sys.exit(1)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("❌ กรุณาติดตั้ง: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        sys.exit(1)

    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(creds, f)

    print(f"✅ Authorization สำเร็จ! บันทึก token ที่ {TOKEN_FILE}")
    print("   ตอนนี้สามารถใช้ DriveImageService ใน src/services/images.py ได้แล้ว")


if __name__ == "__main__":
    authorize()

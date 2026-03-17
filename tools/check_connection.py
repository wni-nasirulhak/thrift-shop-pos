"""
tools/check_connection.py — Verify Google Sheets connection and sheet structure.
Run from project root:  python tools/check_connection.py
"""

import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REQUIRED_SHEETS = [
    "Inventory", "Categories", "Brands", "Sales",
    "Measurements_Shirts", "Measurements_Pants", "Measurements_Shoes",
    "Product_Images",
]


def check():
    print("🔍 ตรวจสอบการเชื่อมต่อ Google Sheets...\n")

    # Check secrets.toml
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    if not os.path.exists(secrets_path):
        print(f"❌ ไม่พบ {secrets_path}")
        print("   กรุณาสร้างไฟล์ .streamlit/secrets.toml ตาม secrets.toml.example")
        sys.exit(1)
    print(f"✅ พบ {secrets_path}")

    try:
        import toml
    except ImportError:
        print("⚠️  pip install toml  (ใช้อ่าน secrets.toml)")
        sys.exit(1)

    with open(secrets_path) as f:
        secrets = toml.load(f)

    if "gcp_service_account" not in secrets or "sheet_name" not in secrets:
        print("❌ secrets.toml ขาด gcp_service_account หรือ sheet_name")
        sys.exit(1)

    print(f"✅ Sheet name: {secrets['sheet_name']}")

    try:
        import gspread
        from google.oauth2.service_account import Credentials

        creds = Credentials.from_service_account_info(
            secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
        )
        client = gspread.authorize(creds)
        workbook = client.open(secrets["sheet_name"])
        print(f"✅ เชื่อมต่อ Google Sheets สำเร็จ!\n")

        existing = {ws.title for ws in workbook.worksheets()}
        for name in REQUIRED_SHEETS:
            status = "✅" if name in existing else "❌ ขาด"
            print(f"  {status}  {name}")

        missing = [n for n in REQUIRED_SHEETS if n not in existing]
        if missing:
            print(f"\n⚠️  Sheets ที่ขาด: {', '.join(missing)}")
            print("   กรุณาสร้างใน Google Sheets ก่อนใช้งาน")
        else:
            print("\n🎉 โครงสร้าง Sheets ครบถ้วน!")

    except Exception as e:
        print(f"❌ เชื่อมต่อไม่สำเร็จ: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check()

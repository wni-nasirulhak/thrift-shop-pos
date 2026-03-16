"""
สคริปต์ย้ายข้อมูลจากชีทเก่าไปชีทใหม่
และเพิ่มคอลัมน์ใหม่
"""

import gspread
from google.oauth2.service_account import Credentials
import json

print("🔄 สคริปต์ย้ายข้อมูล Google Sheet")
print("=" * 50)

# โหลด secrets
try:
    with open('.streamlit/secrets.toml', 'r', encoding='utf-8') as f:
        import toml
        secrets = toml.load(f)
except:
    print("❌ ไม่พบไฟล์ secrets.toml")
    print("💡 กรุณารันจากโฟลเดอร์ที่มีไฟล์ .streamlit/secrets.toml")
    input("กด Enter เพื่อออก...")
    exit(1)

# เชื่อมต่อ Google Sheets
print("\n🔗 กำลังเชื่อมต่อ Google Sheets...")

try:
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    credentials = Credentials.from_service_account_info(
        secrets["gcp_service_account"],
        scopes=scope
    )
    
    client = gspread.authorize(credentials)
    sheet = client.open(secrets["sheet_name"])
    
    print("✅ เชื่อมต่อสำเร็จ!")
except Exception as e:
    print(f"❌ เชื่อมต่อไม่สำเร็จ: {e}")
    input("กด Enter เพื่อออก...")
    exit(1)

# ตรวจสอบว่ามีชีท Inventory หรือไม่
try:
    old_worksheet = sheet.worksheet("Inventory")
    print(f"\n📊 พบชีท 'Inventory' แล้ว")
except:
    print("\n❌ ไม่พบชีท 'Inventory'")
    print("💡 กรุณาสร้างชีท 'Inventory' ก่อนรันสคริปต์นี้")
    input("กด Enter เพื่อออก...")
    exit(1)

# อ่านข้อมูลเก่า
print("\n📖 กำลังอ่านข้อมูลเดิม...")
old_data = old_worksheet.get_all_values()

if len(old_data) <= 1:
    print("⚠️ ไม่มีข้อมูลในชีท (มีแค่ header)")
    print("\n💡 ให้อัปเดต header เป็น:")
    print("Barcode_ID | Item_Name | Brand | Category | Size | Condition | Color | Pattern | Material | Cost | Price | Status | Added_Date | Sold_Date")
    
    # ถามว่าจะอัปเดต header ไหม
    update = input("\nต้องการให้อัปเดต header อัตโนมัติไหม? (y/n): ").lower()
    
    if update == 'y':
        new_header = [
            "Barcode_ID", "Item_Name", "Brand", "Category", "Size", 
            "Condition", "Color", "Pattern", "Material", 
            "Cost", "Price", "Status", "Added_Date", "Sold_Date"
        ]
        
        old_worksheet.clear()
        old_worksheet.append_row(new_header)
        
        print("✅ อัปเดต header สำเร็จ!")
        print("\n🎉 ตอนนี้พร้อมใช้งานแล้ว!")
    else:
        print("\n💡 กรุณาอัปเดต header ด้วยตัวเอง")
    
    input("\nกด Enter เพื่อออก...")
    exit(0)

# ตรวจสอบ header เก่า
old_header = old_data[0]
print(f"📋 Header เดิม ({len(old_header)} คอลัมน์): {old_header}")

# Header ใหม่
new_header = [
    "Barcode_ID", "Item_Name", "Brand", "Category", "Size", 
    "Condition", "Color", "Pattern", "Material", 
    "Cost", "Price", "Status", "Added_Date", "Sold_Date"
]

print(f"📋 Header ใหม่ ({len(new_header)} คอลัมน์): {new_header}")

# ย้ายข้อมูล
print(f"\n🔄 กำลังย้ายข้อมูล {len(old_data) - 1} แถว...")

# สร้างชีทสำรอง
try:
    backup_worksheet = sheet.add_worksheet(title="Inventory_Backup", rows=len(old_data), cols=len(old_header))
    backup_worksheet.update('A1', old_data)
    print("✅ สำรองข้อมูลเดิมไว้ที่ชีท 'Inventory_Backup'")
except:
    print("⚠️ มีชีท 'Inventory_Backup' อยู่แล้ว ข้ามการสำรอง")

# อัปเดตชีทหลัก
new_data = [new_header]

for row in old_data[1:]:
    # แมปข้อมูลเก่าไปใหม่
    new_row = []
    
    # คอลัมน์เดิม (9 คอลัมน์)
    # Barcode_ID, Item_Name, Brand, Size, Cost, Price, Status, Added_Date, Sold_Date
    
    if len(row) >= 9:
        new_row.append(row[0])  # Barcode_ID
        new_row.append(row[1])  # Item_Name
        new_row.append(row[2])  # Brand
        new_row.append("")      # Category (ใหม่ - ว่าง)
        new_row.append(row[3])  # Size
        new_row.append("")      # Condition (ใหม่ - ว่าง)
        new_row.append("")      # Color (ใหม่ - ว่าง)
        new_row.append("")      # Pattern (ใหม่ - ว่าง)
        new_row.append("")      # Material (ใหม่ - ว่าง)
        new_row.append(row[4])  # Cost
        new_row.append(row[5])  # Price
        new_row.append(row[6])  # Status
        new_row.append(row[7])  # Added_Date
        new_row.append(row[8] if len(row) > 8 else "")  # Sold_Date
        
        new_data.append(new_row)
    else:
        print(f"⚠️ ข้ามแถวที่มีข้อมูลไม่ครบ: {row}")

# เขียนข้อมูลใหม่
print("\n💾 กำลังเขียนข้อมูลใหม่...")

old_worksheet.clear()
old_worksheet.update('A1', new_data)

print("✅ อัปเดตสำเร็จ!")

print("\n" + "=" * 50)
print("🎉 Migration เสร็จสมบูรณ์!")
print(f"📊 ย้ายข้อมูล: {len(new_data) - 1} แถว")
print(f"📋 Header ใหม่: {len(new_header)} คอลัมน์")
print("\n💡 ข้อมูลเดิมถูกสำรองไว้ที่ชีท 'Inventory_Backup'")
print("💡 คอลัมน์ใหม่ (Category, Condition, Color, Pattern, Material) จะว่าง")
print("   สามารถกรอกเพิ่มเติมภายหลังได้")

input("\nกด Enter เพื่อออก...")

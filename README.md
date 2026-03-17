# 👕 Thrift Shop POS v4.1

ระบบจุดขาย (POS) + ระบบจัดการรูปภาพ สำหรับร้านเสื้อผ้ามือสอง

**Version:** 4.1 (OAuth 2.0 + Image Management)  
**Status:** ✅ Ready for use

---

## 🚀 Quick Start

### 1. ติดตั้ง Dependencies
```bash
# Windows
2-Install-Dependencies.bat

# หรือ
pip install -r requirements.txt
```

### 2. ตั้งค่า Google Sheets (Service Account)
สร้างไฟล์ `.streamlit/secrets.toml` (ดูตัวอย่างจาก `secrets.toml.example`)

### 3. ตั้งค่า Google Drive (OAuth 2.0)
```bash
# 1. สร้าง OAuth 2.0 credentials (Desktop app) จาก Google Cloud Console
# 2. ดาวน์โหลด JSON → เปลี่ยนชื่อเป็น credentials.json
# 3. รัน authorization
10-Authorize-Drive.bat
```

### 4. Migrate Database
```bash
8-Migrate-Images.bat
```

### 5. รันแอป
```bash
9-Run-App-V4.bat

# หรือ
streamlit run app_v4_images.py
```

เปิดเบราว์เซอร์: **http://localhost:8501**

---

## 📁 โครงสร้างไฟล์

### ไฟล์หลัก
- **app_v4_images.py** - แอปหลัก (Streamlit)
- **image_manager.py** - โมดูลจัดการรูปภาพ (OAuth 2.0)
- **requirements.txt** - Python dependencies

### สคริปต์
- **authorize_drive.py** - OAuth 2.0 authorization สำหรับ Google Drive
- **migrate_images.py** - สร้าง sheets ใหม่ (Product_Images, Social_Posts, Catalog_Settings)
- **fix_image_urls.py** - แก้ URL รูปภาพเก่า

### BAT Files (Windows)
- **2-Install-Dependencies.bat** - ติดตั้ง Python libraries
- **8-Migrate-Images.bat** - สร้าง sheets ใหม่
- **9-Run-App-V4.bat** - รันแอป
- **10-Authorize-Drive.bat** - Authorize Google Drive
- **11-Fix-Image-URLs.bat** - แก้ URL รูปเก่า

### เอกสาร
- **README_V4.md** - คู่มือเต็ม (อ่านก่อน!)
- **QUICK_START_V4.md** - เริ่มต้นใช้งาน 15 นาที
- **CHANGELOG_V4.md** - ประวัติเวอร์ชัน
- **PROJECT_STATUS.md** - สถานะโปรเจกต์

### การตั้งค่า
- **.gitignore** - ป้องกัน sensitive files
- **secrets.toml.example** - ตัวอย่าง secrets
- **credentials.json** - OAuth 2.0 credentials (ห้าม commit!)
- **token.pickle** - OAuth token (ห้าม commit!)

### Archive
- **_archive/** - ไฟล์เก่า (v1.0-v3.0) + docs เก่า

---

## ✨ Features

### Core
- 🏠 **Dashboard** - ภาพรวมยอดขาย
- 📦 **รับของเข้าสต็อก** - บันทึกสินค้า + อัปโหลดรูป (5 รูป) ในหน้าเดียว
- ✏️ **แก้ไขสินค้า** - แก้ข้อมูล + ขนาด + อัปโหลดรูปใหม่
- 🛒 **จุดขายสินค้า** - ขายสินค้า + แสดงรูป
- 🔍 **ค้นหาสินค้า** - ค้นหาจากชื่อ/แบรนด์/รหัส

### Image Management (v4.0+)
- 📸 อัปโหลดรูป 5 รูป/สินค้า
- 🤖 Auto-resize (1200x1200px, 85% quality)
- 📁 โครงสร้างโฟลเดอร์: `YYYY-MM/BARCODE_ID/`
- 🌐 Direct image URLs (Google Drive)
- 🔐 OAuth 2.0 (ใช้ Drive ของ User, 15GB ฟรี!)

---

## 🔑 Authentication

### Google Sheets
- **Service Account** (headless access)
- ตั้งค่าใน `.streamlit/secrets.toml`

### Google Drive
- **OAuth 2.0** (ใช้พื้นที่ของ User)
- ต้อง authorize ครั้งแรก (10-Authorize-Drive.bat)
- Token เก็บใน `token.pickle`

---

## 📖 Documentation

อ่านคู่มือเต็มที่: **README_V4.md**

เริ่มต้นใช้งานที่: **QUICK_START_V4.md**

---

## 🐛 Troubleshooting

### รูปแสดงไม่ได้
```bash
# แก้ URL รูปเก่า
11-Fix-Image-URLs.bat
```

### Token หมดอายุ
```bash
# Authorize ใหม่
10-Authorize-Drive.bat
```

### แอปไม่รัน
```bash
# ติดตั้ง dependencies ใหม่
2-Install-Dependencies.bat
```

---

## 📝 Version History

- **v4.1** (2026-03-17) - OAuth 2.0 hotfix + Edit feature
- **v4.0** (2026-03-16) - Image Management System
- **v3.0** (2026-03-12) - Dynamic forms
- **v2.0** (2026-03-10) - Multi-category
- **v1.0** (2026-03-08) - Initial release

---

**Developed for:** C  
**Last Updated:** 2026-03-17

💝 สนุกกับการใช้งานนะคะ!

# 🚀 คู่มือการติดตั้งและใช้งาน Thrift Shop POS

## 📋 สารบัญ
1. [ติดตั้ง Dependencies](#1-ติดตั้ง-dependencies)
2. [สร้าง Google Sheets](#2-สร้าง-google-sheets)
3. [สร้าง Google Service Account](#3-สร้าง-google-service-account)
4. [ตั้งค่า Secrets](#4-ตั้งค่า-secrets)
5. [รันแอป](#5-รันแอป)
6. [Deploy บน Streamlit Cloud](#6-deploy-บน-streamlit-cloud)

---

## 1. ติดตั้ง Dependencies

### ติดตั้ง Python Libraries
```bash
pip install -r requirements.txt
```

หรือติดตั้งทีละตัว:
```bash
pip install streamlit gspread google-auth pandas qrcode[pil] Pillow
```

---

## 2. สร้าง Google Sheets

### ขั้นตอน:
1. เข้า [Google Sheets](https://sheets.google.com/)
2. สร้าง Spreadsheet ใหม่ ตั้งชื่อว่า **"Thrift Shop Inventory"** (หรือชื่ออื่นตามต้องการ)
3. สร้าง Sheet ชื่อ **"Inventory"** (ต้องชื่อนี้เท่านั้น)
4. เพิ่ม Header ในแถวแรก:

| Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date |
|------------|-----------|-------|------|------|-------|--------|------------|-----------|

**ตัวอย่างข้อมูล:**
| Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date |
|------------|-----------|-------|------|------|-------|--------|------------|-----------|
| 26031612345001 | เสื้อยืดสีขาว | Uniqlo | M | 50 | 150 | Available | 2026-03-16 12:30:00 | |

---

## 3. สร้าง Google Service Account

### ขั้นตอน:
1. เข้า [Google Cloud Console](https://console.cloud.google.com/)
2. สร้างโปรเจกต์ใหม่ หรือเลือกโปรเจกต์ที่มีอยู่
3. เปิดใช้งาน **Google Sheets API**:
   - ไปที่ **APIs & Services** > **Library**
   - ค้นหา "Google Sheets API" แล้วคลิก **Enable**
   - ค้นหา "Google Drive API" แล้วคลิก **Enable** (จำเป็นสำหรับการเข้าถึง Sheets)

4. สร้าง Service Account:
   - ไปที่ **IAM & Admin** > **Service Accounts**
   - คลิก **Create Service Account**
   - ตั้งชื่อ เช่น `thrift-shop-pos`
   - คลิก **Create and Continue**
   - **Skip** การเพิ่ม Role (ไม่จำเป็น)
   - คลิก **Done**

5. สร้าง JSON Key:
   - คลิกที่ Service Account ที่สร้าง
   - ไปที่แท็บ **Keys**
   - คลิก **Add Key** > **Create New Key**
   - เลือก **JSON** แล้วคลิก **Create**
   - ไฟล์ JSON จะดาวน์โหลดอัตโนมัติ (**เก็บไฟล์นี้ไว้ให้ดี อย่าแชร์ใครเด็ดขาด!**)

6. แชร์ Google Sheet กับ Service Account:
   - เปิดไฟล์ JSON ที่ดาวน์โหลดมา
   - หา `client_email` (จะเป็นอีเมลยาวๆ เช่น `thrift-shop-pos@...iam.gserviceaccount.com`)
   - กลับไปที่ Google Sheet ที่สร้างไว้
   - คลิกปุ่ม **Share** (มุมขวาบน)
   - วางอีเมล `client_email` ลงไป
   - เลือก **Editor** (ต้องเป็น Editor ไม่งั้นแอปจะเขียนข้อมูลไม่ได้)
   - คลิก **Send** (อย่าติ๊ก "Notify people")

---

## 4. ตั้งค่า Secrets

### สำหรับรันบน Local (คอมพิวเตอร์ของคุณ):

1. สร้างโฟลเดอร์ `.streamlit` ในโฟลเดอร์โปรเจกต์:
```bash
mkdir .streamlit
```

2. สร้างไฟล์ `.streamlit/secrets.toml`:
```toml
# ชื่อ Google Sheet ที่สร้างไว้
sheet_name = "Thrift Shop Inventory"

# ข้อมูล Service Account (คัดลอกจากไฟล์ JSON)
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

**⚠️ สำคัญ:**
- แทนที่ข้อมูลด้านบนด้วยข้อมูลจากไฟล์ JSON ที่ดาวน์โหลดมา
- `private_key` ต้องรวม `\n` ทุกบรรทัด (ตามที่มีในไฟล์ JSON)
- **อย่าอัปโหลดไฟล์ secrets.toml ขึ้น GitHub เด็ดขาด!** (เพิ่ม `.streamlit/` ใน `.gitignore`)

### ตัวอย่างไฟล์ JSON:
```json
{
  "type": "service_account",
  "project_id": "thrift-shop-123456",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n",
  "client_email": "thrift-shop-pos@thrift-shop-123456.iam.gserviceaccount.com",
  ...
}
```

---

## 5. รันแอป

### รันบน Local:
```bash
streamlit run app.py
```

แอปจะเปิดที่ `http://localhost:8501` 🎉

---

## 6. Deploy บน Streamlit Cloud (ฟรี!)

### ขั้นตอน:

1. **อัปโหลดโค้ดขึ้น GitHub:**
   - สร้าง Repository ใหม่บน GitHub
   - Push โค้ดขึ้นไป (อย่าลืม `.gitignore` ไฟล์ secrets!)
   
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/thrift-shop-pos.git
   git push -u origin main
   ```

2. **Deploy บน Streamlit Cloud:**
   - ไปที่ [share.streamlit.io](https://share.streamlit.io/)
   - Sign in ด้วย GitHub
   - คลิก **New app**
   - เลือก Repository, Branch, และ Main file (`app.py`)
   - คลิก **Advanced settings**
   - เพิ่ม Secrets โดยคัดลอกเนื้อหาจาก `.streamlit/secrets.toml` ใส่ลงไป
   - คลิก **Deploy!**

3. **แอปจะออนไลน์ภายใน 2-3 นาที** 🚀
   - URL จะเป็น `https://your-app-name.streamlit.app`
   - แชร์ URL นี้ให้ทีมงานใช้ได้เลย!

---

## 📱 การใช้งานบนมือถือ

แอปนี้ใช้งานได้ดีบนมือถือ:
- เปิด URL ของแอปผ่านเบราว์เซอร์มือถือ
- ช่อง "สแกนหรือพิมพ์รหัสสินค้า" สามารถใช้แอปสแกน QR Code ภายนอกแล้วนำรหัสมาวาง
- หรือใช้เบราว์เซอร์ที่รองรับ camera permission (เช่น Chrome) เพื่อสแกนด้วย Web Barcode Scanner

---

## 🛠️ Troubleshooting

### ❌ "Authentication failed"
- ตรวจสอบว่า Service Account JSON ถูกต้อง
- ตรวจสอบว่าได้ Share Google Sheet ให้กับ `client_email` แล้ว (เป็น Editor)
- ตรวจสอบว่าได้ Enable Google Sheets API และ Google Drive API แล้ว

### ❌ "Worksheet 'Inventory' not found"
- ตรวจสอบว่าสร้าง Sheet ชื่อ "Inventory" แล้ว (ต้องชื่อนี้เท่านั้น)
- ตรวจสอบว่าตั้งชื่อ Spreadsheet ใน `secrets.toml` ถูกต้อง

### ❌ "ModuleNotFoundError"
- ติดตั้ง dependencies: `pip install -r requirements.txt`

---

## 📞 ติดต่อ & สนับสนุน

หากมีปัญหาหรือข้อสงสัย สามารถสอบถามได้เลยครับ! 💝

---

**ขอให้ใช้งานระบบ POS อย่างมีความสุข! 🎉**

# 📱 คู่มือทีละขั้นตอน - ทำตามได้แน่นอน!

## 🎯 ก่อนเริ่ม
- เปิดคู่มือนี้ไว้ข้างๆ
- เตรียม Gmail account
- ใช้เวลาประมาณ 10-15 นาที

---

## ขั้นตอนที่ 1: สร้าง Google Sheet 📊

### 1.1 สร้าง Spreadsheet
1. เปิดเบราว์เซอร์ไปที่: https://sheets.google.com
2. กดปุ่ม **"+"** (Blank spreadsheet) เพื่อสร้างใหม่
3. มุมซ้ายบน คลิกที่ "Untitled spreadsheet" 
4. ตั้งชื่อว่า: **Thrift Shop Inventory** (เป๊ะๆ)
5. กด Enter

### 1.2 เปลี่ยนชื่อ Sheet
1. มุมล่างซ้าย จะมี "Sheet1"
2. คลิกขวาที่ "Sheet1" → เลือก **Rename**
3. ตั้งชื่อใหม่เป็น: **Inventory** (เป๊ะๆ ห้ามผิด!)
4. กด Enter

### 1.3 ใส่ Header
พิมพ์ข้อความต่อไปนี้ในแต่ละช่อง (แถวที่ 1):

| A1 | B1 | C1 | D1 | E1 | F1 | G1 | H1 | I1 |
|---|---|---|---|---|---|---|---|---|
| Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date |

✅ **เช็คให้แน่ใจ:** ต้องมี 9 คอลัมน์ ชื่อต้องเหมือนกันทุกตัวอักษร!

คัดลอกง่ายๆ (วาง 9 ช่องนี้ในแถวแรก):
```
Barcode_ID	Item_Name	Brand	Size	Cost	Price	Status	Added_Date	Sold_Date
```

### 1.4 เก็บ URL ไว้
คัดลอก URL ของ Google Sheet นี้ไว้ (จะใช้ภายหลัง)
ตัวอย่าง: `https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9/edit`

---

## ขั้นตอนที่ 2: สร้าง Google Cloud Project & Service Account ☁️

### 2.1 เข้า Google Cloud Console
1. เปิดเบราว์เซอร์ไปที่: https://console.cloud.google.com
2. ถ้าถามให้ยอมรับ Terms of Service → คลิก **Agree and Continue**

### 2.2 สร้าง Project ใหม่
1. มุมบนซ้าย (ข้างโลโก้ Google Cloud) จะมี dropdown **"Select a project"**
2. คลิก dropdown นั้น
3. คลิกปุ่ม **"NEW PROJECT"** (มุมขวาบนของ popup)
4. กรอกข้อมูล:
   - **Project name:** `Thrift Shop POS` (หรือชื่ออะไรก็ได้)
   - **Location:** ไม่ต้องแก้
5. คลิก **CREATE**
6. รอ 5-10 วินาที จนกว่าจะสร้างเสร็จ
7. เลือก Project ที่สร้างใหม่จาก dropdown (บนซ้าย)

### 2.3 เปิดใช้งาน Google Sheets API
1. เมนูซ้าย → คลิก **"APIs & Services"** → **"Library"**
2. ช่องค้นหา พิมพ์: **Google Sheets API**
3. คลิกที่ **Google Sheets API** (อันแรกที่ขึ้นมา)
4. คลิกปุ่ม **ENABLE** (สีน้ำเงิน)
5. รอจนปุ่มเปลี่ยนเป็น **MANAGE** → เสร็จแล้ว!

### 2.4 เปิดใช้งาน Google Drive API
1. กดลูกศรย้อนกลับ (หรือเมนูซ้าย → **Library**)
2. ช่องค้นหา พิมพ์: **Google Drive API**
3. คลิกที่ **Google Drive API**
4. คลิกปุ่ม **ENABLE**
5. รอจนเสร็จ

### 2.5 สร้าง Service Account
1. เมนูซ้าย → **"IAM & Admin"** → **"Service Accounts"**
2. คลิกปุ่ม **"+ CREATE SERVICE ACCOUNT"** (บนสุด)
3. กรอกข้อมูล:
   - **Service account name:** `thrift-pos` (หรือชื่ออะไรก็ได้)
   - **Service account ID:** จะสร้างอัตโนมัติ (ไม่ต้องแก้)
   - **Description:** ไม่ใส่ก็ได้
4. คลิก **CREATE AND CONTINUE**
5. หน้า "Grant this service account access to project":
   - **ข้ามไป ไม่ต้องเลือกอะไร**
   - คลิก **CONTINUE**
6. หน้า "Grant users access to this service account":
   - **ข้ามไป ไม่ต้องเลือกอะไร**
   - คลิก **DONE**

### 2.6 ดาวน์โหลด JSON Key
1. จะเห็น Service Account ที่สร้างในตาราง
2. คลิกที่ Service Account (แถวที่สร้าง)
3. ไปที่แท็บ **"KEYS"** (บนสุด)
4. คลิก **"ADD KEY"** → **"Create new key"**
5. เลือก **JSON** (ต้องเป็น JSON!)
6. คลิก **CREATE**
7. ไฟล์ JSON จะดาวน์โหลดมา (ชื่อยาวๆ เช่น `thrift-shop-pos-123456-abc.json`)
8. **เก็บไฟล์นี้ไว้ในที่ปลอดภัย!** (ย้ายไปไว้ในโฟลเดอร์โปรเจกต์)

### 2.7 แชร์ Google Sheet ให้ Service Account
1. เปิดไฟล์ JSON ที่ดาวน์โหลดมาด้วย Notepad
2. หาบรรทัดที่มีคำว่า `"client_email"`
3. คัดลอกอีเมลทั้งหมด (จะยาวๆ เช่น `thrift-pos@thrift-shop-pos-123456.iam.gserviceaccount.com`)
4. กลับไปที่ Google Sheet ที่สร้างไว้
5. คลิกปุ่ม **Share** (มุมขวาบน สีเขียว)
6. วางอีเมล `client_email` ในช่อง "Add people and groups"
7. เลือก dropdown ด้านขวา → เลือก **Editor** (ต้องเป็น Editor!)
8. **ยกเลิกติ๊ก** "Notify people" (ไม่ต้องส่งอีเมลแจ้ง)
9. คลิก **Share**

✅ **เสร็จขั้นตอนที่ 2 แล้ว!** Service Account สามารถเข้าถึง Google Sheet แล้ว

---

## ขั้นตอนที่ 3: สร้างไฟล์ secrets.toml 🔐

### 3.1 สร้างโฟลเดอร์ .streamlit
1. เปิด File Explorer ไปที่โฟลเดอร์โปรเจกต์: `C:\Users\Winon\.openclaw\workspace\thrift-shop-pos`
2. คลิกขวาในพื้นที่ว่าง → **New** → **Folder**
3. ตั้งชื่อว่า: `.streamlit` (ต้องมีจุดข้างหน้า!)
   - ถ้า Windows ไม่ให้ตั้งชื่อที่มีจุด: เปิด Command Prompt แล้วพิมพ์ `mkdir .streamlit`

### 3.2 ย้ายไฟล์ JSON
1. ย้ายไฟล์ JSON ที่ดาวน์โหลดมาไว้ในโฟลเดอร์โปรเจกต์
2. เปลี่ยนชื่อเป็น: `service-account.json` (จะได้จำง่าย)

### 3.3 รันสคริปต์สร้าง secrets.toml อัตโนมัติ
ใช้สคริปต์ Python ที่น้องดาเตรียมไว้ให้ (ด้านล่าง) จะสร้างไฟล์ `secrets.toml` ให้อัตโนมัติ!

---

## ขั้นตอนที่ 4: รันแอป 🚀

หลังจากสร้าง `secrets.toml` เสร็จแล้ว:

```bash
cd C:\Users\Winon\.openclaw\workspace\thrift-shop-pos
streamlit run app.py
```

เบราว์เซอร์จะเปิดที่ `http://localhost:8501` 🎉

---

## 🆘 ติดปัญหา?

### "Authentication failed"
- ตรวจสอบว่าได้ Share Google Sheet ให้ `client_email` แล้ว (เป็น Editor)
- ตรวจสอบว่าได้ Enable ทั้ง Google Sheets API และ Google Drive API แล้ว

### "Worksheet not found"
- ตรวจสอบว่าตั้งชื่อ Sheet ว่า "Inventory" (ไม่ใช่ Sheet1)
- ตรวจสอบว่า `sheet_name` ใน `secrets.toml` ตรงกับชื่อ Spreadsheet

### "Module not found"
- รัน: `pip install -r requirements.txt`

---

**ทำตามนี้แล้วได้แน่นอนค่ะ! มีปัญหาถามน้องดาได้เลยนะ 💝**

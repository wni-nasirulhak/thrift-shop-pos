# ⚡ Quick Start Guide (ฉบับเร่งด่วน!)

ถ้าอยากเริ่มใช้งานเร็วที่สุด ทำตามนี้เลย! 🚀

---

## ✅ สิ่งที่ต้องเตรียม
- [ ] Python 3.8 ขึ้นไป (ติดตั้งแล้ว)
- [ ] บัญชี Google (Gmail)
- [ ] Internet

---

## 🔥 5 ขั้นตอนสู่การใช้งาน

### 1️⃣ ติดตั้ง Libraries (2 นาที)
เปิด Terminal/CMD แล้วพิมพ์:
```bash
cd thrift-shop-pos
pip install streamlit gspread google-auth pandas qrcode[pil] Pillow
```

รอจนเสร็จ ✅

---

### 2️⃣ สร้าง Google Sheet (3 นาที)

1. เข้า [sheets.google.com](https://sheets.google.com)
2. สร้าง Spreadsheet ใหม่ ตั้งชื่อ **"Thrift Shop Inventory"**
3. ตั้งชื่อ Sheet แรกว่า **"Inventory"** (ตรงนี้สำคัญ!)
4. พิมพ์ header ในแถวแรก (A1-I1):
   ```
   Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date
   ```

ตัวอย่าง:
| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date |

---

### 3️⃣ สร้าง Service Account (5 นาที)

#### 3.1 เปิดใช้งาน API
1. เข้า [console.cloud.google.com](https://console.cloud.google.com)
2. สร้างโปรเจกต์ใหม่ (ถ้ายังไม่มี) ตั้งชื่ออะไรก็ได้ เช่น "Thrift Shop"
3. ไปที่ **APIs & Services > Library**
4. ค้นหา **"Google Sheets API"** → คลิก **Enable**
5. ค้นหา **"Google Drive API"** → คลิก **Enable**

#### 3.2 สร้าง Service Account
1. ไปที่ **IAM & Admin > Service Accounts**
2. คลิก **Create Service Account**
3. ตั้งชื่อ: `thrift-pos` (หรืออะไรก็ได้)
4. คลิก **Create and Continue** → **Done** (ข้าม Grant access)

#### 3.3 ดาวน์โหลด JSON Key
1. คลิกที่ Service Account ที่สร้าง
2. ไปที่แท็บ **Keys**
3. คลิก **Add Key > Create New Key**
4. เลือก **JSON** → **Create**
5. ไฟล์ JSON จะดาวน์โหลดมา → **เก็บไว้ดีๆ อย่าให้ใครได้!**

#### 3.4 แชร์ Sheet
1. เปิดไฟล์ JSON ที่ดาวน์โหลดมา (ใช้ Notepad)
2. หาบรรทัด `"client_email"` คัดลอกอีเมล (จะยาวๆ)
3. กลับไปที่ Google Sheet
4. คลิกปุ่ม **Share** (มุมขวาบน)
5. วางอีเมล `client_email` ลงไป
6. เลือก **Editor** (ต้องเป็น Editor!)
7. **ยกเลิกติ๊ก** "Notify people"
8. คลิก **Share**

---

### 4️⃣ ตั้งค่า Secrets (3 นาที)

1. สร้างโฟลเดอร์ `.streamlit` ในโฟลเดอร์โปรเจกต์:
   - Windows: เปิด File Explorer → สร้างโฟลเดอร์ชื่อ `.streamlit`
   - Mac/Linux: `mkdir .streamlit`

2. สร้างไฟล์ชื่อ `secrets.toml` ใน `.streamlit/`

3. เปิดไฟล์ JSON ที่ดาวน์โหลด + เปิดไฟล์ `secrets.toml` ด้วย Notepad

4. คัดลอกข้อมูลจาก JSON ไปใส่ใน `secrets.toml` ตามรูปแบบนี้:

```toml
sheet_name = "Thrift Shop Inventory"

[gcp_service_account]
type = "service_account"
project_id = "คัดลอกจาก JSON"
private_key_id = "คัดลอกจาก JSON"
private_key = "คัดลอกจาก JSON (รวม \\n ทุกบรรทัด)"
client_email = "คัดลอกจาก JSON"
client_id = "คัดลอกจาก JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "คัดลอกจาก JSON"
universe_domain = "googleapis.com"
```

**⚠️ สำคัญ:** ใน `private_key` ต้องมี `\n` ตามที่มีในไฟล์ JSON (อย่าลบ!)

ตัวอย่าง:
```toml
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqh...\n-----END PRIVATE KEY-----\n"
```

5. บันทึกไฟล์

---

### 5️⃣ รันแอป! (10 วินาที)

```bash
streamlit run app.py
```

เบราว์เซอร์จะเปิดอัตโนมัติที่ `http://localhost:8501` 🎉

---

## 🎯 ทดสอบการใช้งาน

### เพิ่มสินค้าทดสอบ:
1. เลือกเมนู **"📦 รับของเข้าสต็อก"**
2. กรอกข้อมูล:
   - ชื่อสินค้า: เสื้อยืดสีขาว
   - แบรนด์: Uniqlo
   - ไซส์: M
   - ต้นทุน: 50
   - ราคาขาย: 150
3. คลิก **บันทึก**
4. ระบบจะสร้าง QR Code ให้ → ดาวน์โหลดไว้

### ขายสินค้า:
1. เลือกเมนู **"🛒 จุดขายสินค้า"**
2. ใส่รหัสสินค้า (หรือสแกน QR Code)
3. คลิก **ยืนยันการขาย**
4. เสร็จสิ้น! 🎉

### ดู Dashboard:
1. เลือกเมนู **"🏠 Dashboard"**
2. ดูสถิติ กำไร และสต็อกคงเหลือ

---

## ❓ ติดปัญหา?

### ไม่เชื่อมต่อ Google Sheets
- ✅ ตรวจสอบว่าได้ Enable API ทั้ง Sheets และ Drive แล้ว
- ✅ ตรวจสอบว่าได้ Share Sheet ให้ `client_email` (เป็น Editor) แล้ว
- ✅ ตรวจสอบว่าตั้งชื่อ Sheet ว่า "Inventory" แล้ว
- ✅ ตรวจสอบว่า `secrets.toml` มี `private_key` ครบถ้วน (รวม `\n`)

### ไม่เจอ Worksheet
- ✅ ตรวจสอบว่าชื่อ Sheet คือ **"Inventory"** (ต้องเป๊ะ!)
- ✅ ตรวจสอบว่า `sheet_name` ใน `secrets.toml` ตรงกับชื่อ Spreadsheet

### อื่นๆ
- อ่านคู่มือฉบับเต็ม: [SETUP.md](SETUP.md)
- หรือถามได้เลย! 💝

---

**เรียบร้อย! ใช้งานได้แล้ว! 🎊**

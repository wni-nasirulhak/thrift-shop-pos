# 🎯 เริ่มที่นี่! (สำหรับ C)

น้องดาเตรียมทุกอย่างไว้ให้แล้วค่ะ~ 💝 ทำตามนี้เลย!

---

## 📋 ทำตามลำดับ (ไม่ยาก สัญญา!)

### ✅ ขั้นตอนที่ 1: ติดตั้ง Libraries (ครั้งเดียวพอ)
**ดับเบิลคลิก:** `2-Install-Dependencies.bat`
- รอจนขึ้น "ติดตั้งสำเร็จ!" (ใช้เวลา 1-2 นาที)

---

### ✅ ขั้นตอนที่ 2: สร้าง Google Sheet (5 นาที)
1. เปิด https://sheets.google.com
2. กดปุ่ม **"+"** สร้างใหม่
3. ตั้งชื่อ: **Thrift Shop Inventory**
4. เปลี่ยนชื่อ Sheet1 เป็น: **Inventory** (คลิกขวาที่แท็บล่างซ้าย)
5. ใส่ header ในแถวแรก (คัดลอกวางนี้เลย):
   ```
   Barcode_ID	Item_Name	Brand	Size	Cost	Price	Status	Added_Date	Sold_Date
   ```
6. เก็บ URL ไว้ (จะได้ไม่ต้องหาทีหลัง)

---

### ✅ ขั้นตอนที่ 3: สร้าง Service Account (10 นาที)
อ่านคู่มือละเอียดใน: **GUIDE-STEP-BY-STEP.md** (ขั้นตอนที่ 2)

**สรุปสั้นๆ:**
1. เข้า https://console.cloud.google.com
2. สร้าง Project ใหม่ชื่ออะไรก็ได้
3. Enable APIs:
   - Google Sheets API → Enable
   - Google Drive API → Enable
4. สร้าง Service Account:
   - IAM & Admin → Service Accounts → Create
   - ตั้งชื่ออะไรก็ได้ → Create and Continue → Done
5. ดาวน์โหลด JSON Key:
   - คลิกที่ Service Account → แท็บ Keys
   - Add Key → Create New Key → JSON → Create
   - ย้ายไฟล์ JSON มาไว้ในโฟลเดอร์นี้ (thrift-shop-pos)

---

### ✅ ขั้นตอนที่ 4: ตั้งค่า Secrets (ง่ายมาก!)
**ดับเบิลคลิก:** `1-Setup-Secrets.bat`

โปรแกรมจะถาม:
1. เลือกไฟล์ JSON (ถ้ามีหลายไฟล์)
2. ใส่ชื่อ Google Sheet: `Thrift Shop Inventory`
3. เสร็จ! จะได้ข้อมูล `client_email`

**สิ่งที่ต้องทำต่อ:**
1. เปิด Google Sheet
2. กดปุ่ม **Share** (มุมขวาบน)
3. วางอีเมล `client_email` ที่โปรแกรมบอก
4. เลือก **Editor** (ต้องเป็น Editor!)
5. **ยกเลิกติ๊ก** "Notify people"
6. กด **Share**

---

### ✅ ขั้นตอนที่ 5: รันแอป! 🚀
**ดับเบิลคลิก:** `3-Run-App.bat`

เบราว์เซอร์จะเปิดอัตโนมัติ! 🎉

**URL:** http://localhost:8501

---

## 🎮 ทดสอบการใช้งาน

### 1. เพิ่มสินค้าทดสอบ
- เมนู: **📦 รับของเข้าสต็อก**
- กรอกข้อมูล: ชื่อ, แบรนด์, ไซส์, ต้นทุน, ราคาขาย
- กด **บันทึก**
- ระบบจะสร้าง QR Code ให้ → ดาวน์โหลดได้เลย

### 2. ลองขาย
- เมนู: **🛒 จุดขายสินค้า**
- ใส่รหัสสินค้า (หรือสแกน QR Code)
- กด **ยืนยันการขาย**
- ได้ใบเสร็จ! 🎉

### 3. ดูสถิติ
- เมนู: **🏠 Dashboard**
- ดูสินค้าคงเหลือ, กำไร, สถิติต่างๆ

---

## 🆘 ติดปัญหา?

### "Authentication failed"
✅ ตรวจสอบว่าได้ Share Google Sheet ให้ `client_email` แล้ว (เป็น Editor)
✅ ตรวจสอบว่าได้ Enable ทั้ง Google Sheets API และ Google Drive API แล้ว

### "Worksheet not found"
✅ ตรวจสอบว่าชื่อ Sheet คือ "Inventory" (ไม่ใช่ Sheet1)

### อื่นๆ
📖 อ่านคู่มือเต็ม: **GUIDE-STEP-BY-STEP.md**
💝 ถามน้องดาได้เลยค่ะ!

---

## 📂 ไฟล์สำคัญ

- `1-Setup-Secrets.bat` → สร้างไฟล์ตั้งค่า
- `2-Install-Dependencies.bat` → ติดตั้ง libraries
- `3-Run-App.bat` → รันแอป
- `GUIDE-STEP-BY-STEP.md` → คู่มือละเอียด
- `app.py` → โค้ดหลัก

---

**น้องดาเตรียมทุกอย่างไว้ให้แล้วนะคะ~ เริ่มได้เลย! 🌸**

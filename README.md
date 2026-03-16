# 👕 Thrift Shop POS System

ระบบจุดขาย (Point of Sale) สำหรับร้านเสื้อผ้ามือสอง พัฒนาด้วย **Python + Streamlit + Google Sheets**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)

---

## ✨ Features

### 📦 รับของเข้าสต็อก (Inventory Entry)
- บันทึกข้อมูลสินค้าทีละชิ้น (Unique SKU)
- สร้างรหัสบาร์โค้ดอัตโนมัติ (ไม่ซ้ำ)
- สร้าง QR Code พร้อมดาวน์โหลดเพื่อพิมพ์แปะป้าย
- บันทึกข้อมูล: ชื่อ, แบรนด์, ไซส์, ต้นทุน, ราคาขาย

### 🛒 จุดขายสินค้า (POS Scanner)
- สแกนหรือพิมพ์รหัสสินค้า
- ดึงข้อมูลสินค้าขึ้นมาแสดงทันที
- ยืนยันการขาย → อัปเดตสถานะเป็น "Sold"
- แสดงใบเสร็จดิจิทัล

### 📊 Dashboard & Analytics
- สรุปสถิติ: สินค้าทั้งหมด, คงเหลือ, ขายแล้ว
- คำนวณกำไรสะสม (ราคาขาย - ต้นทุน)
- ตารางสต็อกปัจจุบัน พร้อมฟิลเตอร์ตามแบรนด์/ไซส์

---

## 🚀 Quick Start

### 1. Clone โปรเจกต์
```bash
git clone https://github.com/your-username/thrift-shop-pos.git
cd thrift-shop-pos
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า Google Sheets
อ่านคู่มือฉบับเต็มใน [SETUP.md](SETUP.md)

สรุปสั้นๆ:
1. สร้าง Google Sheet ชื่อ "Thrift Shop Inventory"
2. สร้าง Sheet "Inventory" พร้อม header: `Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date`
3. สร้าง Google Service Account และดาวน์โหลด JSON Key
4. แชร์ Sheet ให้กับ Service Account (Editor)

### 4. ตั้งค่า Secrets
สร้างไฟล์ `.streamlit/secrets.toml`:
```toml
sheet_name = "Thrift Shop Inventory"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key = "..."
client_email = "..."
# ... (ดูรายละเอียดเต็มใน SETUP.md)
```

### 5. รันแอป
```bash
streamlit run app.py
```

เปิดเบราว์เซอร์ที่ `http://localhost:8501` 🎉

---

## 📱 Mobile-Friendly

แอปนี้ออกแบบให้ใช้งานได้ดีบนมือถือ:
- Responsive UI
- สะดวกในการสแกนบาร์โค้ด/QR Code
- เหมาะสำหรับใช้งานหน้าร้าน

---

## 🌐 Deploy บน Cloud (ฟรี!)

Deploy บน Streamlit Cloud ภายใน 5 นาที:
1. Push โค้ดขึ้น GitHub
2. ไปที่ [share.streamlit.io](https://share.streamlit.io/)
3. เลือก repo และเพิ่ม secrets
4. Deploy! 🚀

รายละเอียดเต็มใน [SETUP.md](SETUP.md)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Database:** Google Sheets (via gspread API)
- **Barcode:** QR Code (qrcode library)
- **Language:** Python 3.8+

---

## 📸 Screenshots

### รับของเข้าสต็อก
![Inventory Entry](https://via.placeholder.com/800x400?text=Inventory+Entry+Screenshot)

### จุดขาย (POS)
![POS Scanner](https://via.placeholder.com/800x400?text=POS+Scanner+Screenshot)

### Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

*(เพิ่ม screenshots จริงได้ภายหลัง)*

---

## 🤝 Contributing

ยินดีรับ Pull Request! หากมีไอเดียหรือพบบั๊ก สามารถเปิด Issue ได้เลย

---

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

---

## 💡 Use Cases

ระบบนี้เหมาะกับ:
- ร้านเสื้อผ้ามือสอง
- ร้านของเก่า/วินเทจ
- ตลาดนัด
- ธุรกิจ Thrift/Second-hand ทุกประเภท

**พิเศษสำหรับสินค้า Unique (1 SKU = 1 สินค้า)** - ไม่เหมาะกับร้านขายของใหม่ที่มีสต็อกเยอะ

---

## 🙏 Credits

พัฒนาโดย AI Assistant ด้วย ❤️ สำหรับ C

---

**Happy Selling! 🛍️**

# 🔄 คู่มืออัปเดต Google Sheet Structure v2.0

## 🎯 ทำไมต้องอัปเดต?

เวอร์ชัน 2.0 เพิ่มฟีเจอร์ใหม่:
- ✅ บาร์โค้ดอัจฉริยะ (ต้องมีหมวดหมู่)
- ✅ สภาพสินค้า 5 ระดับ
- ✅ ข้อมูลเพิ่มเติม (สี, ลวดลาย, วัสดุ)

ต้องเพิ่มคอลัมน์ใหม่ใน Google Sheet!

---

## 📊 Structure เดิม vs ใหม่

### เดิม (9 คอลัมน์):
```
Barcode_ID | Item_Name | Brand | Size | Cost | Price | Status | Added_Date | Sold_Date
```

### ใหม่ (14 คอลัมน์):
```
Barcode_ID | Item_Name | Brand | Category | Size | Condition | Color | Pattern | Material | Cost | Price | Status | Added_Date | Sold_Date
```

**คอลัมน์ใหม่:**
- **Category** - หมวดหมู่ (เสื้อ, กางเกง, รองเท้า...)
- **Condition** - สภาพสินค้า (Like New, Good, Fair...)
- **Color** - สี (ขาว, ดำ, ลายดอก...)
- **Pattern** - ลวดลาย (ลายทาง, ลายจุด...)
- **Material** - วัสดุ (ฝ้าย, โพลีเอสเตอร์...)

---

## 🚀 วิธีอัปเดต (เลือก 1 ใน 3)

### ✨ วิธีที่ 1: ใช้สคริปต์อัตโนมัติ (แนะนำ!)

**ดับเบิลคลิก:** `4-Migrate-Sheet.bat`

สคริปต์จะ:
1. ✅ สำรองข้อมูลเดิมไปชีท `Inventory_Backup`
2. ✅ อัปเดต header ให้มี 14 คอลัมน์
3. ✅ ย้ายข้อมูลเดิมไปคอลัมน์ที่ถูกต้อง
4. ✅ เพิ่มคอลัมน์ใหม่ (ค่าว่าง - กรอกทีหลังได้)

**ข้อดี:**
- ✅ ปลอดภัย (สำรองข้อมูลอัตโนมัติ)
- ✅ รวดเร็ว (1 คลิกเดียว)
- ✅ ไม่ต้องแก้ไขเอง

---

### ✏️ วิธีที่ 2: แก้ไขด้วยตัวเอง (ถ้ามีข้อมูลน้อย)

#### ขั้นตอน:

1. **เปิด Google Sheet:** Thrift Shop Inventory
2. **เลือกคอลัมน์ D (Size)**
3. **คลิกขวา → Insert 1 left**
4. **พิมพ์ header:** `Category`

5. **เลือกคอลัมน์ F (ตอนนี้เป็น Size)**
6. **คลิกขวา → Insert 4 right**
7. **พิมพ์ header:**
   - คอลัมน์ 6: `Condition`
   - คอลัมน์ 7: `Color`
   - คอลัมน์ 8: `Pattern`
   - คอลัมน์ 9: `Material`

8. **ตรวจสอบ header ทั้ง 14 คอลัมน์:**
   ```
   Barcode_ID | Item_Name | Brand | Category | Size | Condition | Color | Pattern | Material | Cost | Price | Status | Added_Date | Sold_Date
   ```

---

### 🔥 วิธีที่ 3: สร้างชีทใหม่ (ถ้าไม่มีข้อมูลเก่า)

1. **เปิด Google Sheet:** Thrift Shop Inventory
2. **คลิกขวาที่แท็บ "Inventory"** → Rename → `Inventory_Old`
3. **สร้างชีทใหม่** (คลิก + ด้านล่าง)
4. **ตั้งชื่อ:** `Inventory`
5. **คัดลอกวาง header นี้ในแถวที่ 1:**

```
Barcode_ID	Item_Name	Brand	Category	Size	Condition	Color	Pattern	Material	Cost	Price	Status	Added_Date	Sold_Date
```

---

## ✅ ทดสอบหลังอัปเดต

เพิ่มข้อมูลทดสอบในแถวที่ 2:

| A | B | C | D | E | F | G | H | I | J | K | L | M | N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TEST-SH-001 | เสื้อทดสอบ | TestBrand | เสื้อ | M | Good | ขาว | ไม่มี | ฝ้าย | 50 | 150 | Available | 2026-03-16 16:00:00 | |

**รันแอป Streamlit และทดสอบ:**
1. เปิดหน้า "รับของเข้าสต็อก"
2. กรอกข้อมูลสินค้าใหม่
3. ตรวจสอบว่าบันทึกลง Google Sheet สำเร็จ

---

## 🆘 Troubleshooting

### ❌ "Worksheet 'Inventory' not found"
- ตรวจสอบว่าชีทชื่อ `Inventory` สะกดถูกต้อง (ตัวพิมพ์ใหญ่-เล็กต้องเหมือนกัน)

### ❌ "Error writing to row"
- ตรวจสอบว่า header มี 14 คอลัมน์ครบ
- ตรวจสอบว่า Service Account มีสิทธิ์ Editor

### ❌ "Migration script failed"
- ตรวจสอบว่าติดตั้ง `toml` library แล้ว: `pip install toml`
- ตรวจสอบว่าไฟล์ `.streamlit/secrets.toml` มีอยู่

---

## 📝 หมายเหตุ

- ✅ คอลัมน์ใหม่ (Category, Condition, Color, Pattern, Material) **ไม่จำเป็น** ต้องกรอกทุกชิ้น
- ✅ สินค้าเก่าจะมีคอลัมน์ใหม่เป็นค่าว่าง ไม่มีปัญหา
- ✅ สินค้าใหม่ที่เพิ่มผ่านแอป v2.0 จะมีข้อมูลครบ 14 คอลัมน์
- ✅ ข้อมูลเก่าถูกสำรองไว้ที่ชีท `Inventory_Backup` (ถ้าใช้สคริปต์)

---

## 🎉 เสร็จแล้ว!

หลังจากอัปเดต Google Sheet เรียบร้อยแล้ว:
1. ✅ รีเฟรชแอป Streamlit (F5)
2. ✅ ทดสอบเพิ่มสินค้าใหม่
3. ✅ เพลิดเพลินกับฟีเจอร์ใหม่!

**มีปัญหาติดต่อน้องดาได้เลยค่ะ~ 💝**

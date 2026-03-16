"""
POS System สำหรับร้านเสื้อผ้ามือสอง
ใช้ Streamlit + Google Sheets
พัฒนาโดย: AI Assistant
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import qrcode
from io import BytesIO
import time

# ===== การตั้งค่าหน้าเว็บ =====
st.set_page_config(
    page_title="Thrift Shop POS",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== ฟังก์ชันเชื่อมต่อ Google Sheets =====
@st.cache_resource
def connect_to_sheets():
    """
    เชื่อมต่อกับ Google Sheets ผ่าน Service Account
    ใช้ st.secrets เพื่อเก็บข้อมูลการเชื่อมต่ออย่างปลอดภัย
    """
    try:
        # กำหนด scope สำหรับ Google Sheets API
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # ดึงข้อมูลจาก secrets (จะอธิบายการตั้งค่าด้านล่าง)
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        
        # สร้าง client สำหรับเชื่อมต่อ
        client = gspread.authorize(credentials)
        
        # เปิด Google Sheet ตามชื่อที่กำหนด
        sheet = client.open(st.secrets["sheet_name"])
        
        return sheet
    except Exception as e:
        st.error(f"❌ เชื่อมต่อ Google Sheets ไม่สำเร็จ: {e}")
        st.info("💡 กรุณาตรวจสอบการตั้งค่า secrets.toml และสิทธิ์การเข้าถึง Sheet")
        return None

# ===== ฟังก์ชันสร้างรหัสบาร์โค้ด =====
def generate_barcode_id():
    """
    สร้างรหัสสินค้าแบบ Unique จากวันเวลาปัจจุบัน
    รูปแบบ: YYMMDDHHMMSSmmm (ปี เดือน วัน ชั่วโมง นาที วินาที มิลลิวินาที)
    เช่น: 26031614485512345
    """
    now = datetime.now()
    barcode = now.strftime("%y%m%d%H%M%S") + str(now.microsecond)[:3]
    return barcode

# ===== ฟังก์ชันสร้าง QR Code =====
def generate_qr_code(data):
    """
    สร้าง QR Code จากข้อมูลที่กำหนด
    Return: BytesIO object ที่สามารถแสดงใน Streamlit ได้
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # แปลงเป็น BytesIO เพื่อแสดงใน Streamlit
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ===== ฟังก์ชันบันทึกข้อมูลสินค้า =====
def add_inventory_item(sheet, barcode_id, item_name, brand, size, cost, price):
    """
    เพิ่มสินค้าใหม่เข้าสู่ Google Sheets
    """
    try:
        worksheet = sheet.worksheet("Inventory")
        
        # สร้างแถวข้อมูลใหม่
        new_row = [
            barcode_id,
            item_name,
            brand,
            size,
            float(cost),
            float(price),
            "Available",  # สถานะเริ่มต้น
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Added_Date
            ""  # Sold_Date (ยังไม่มี)
        ]
        
        worksheet.append_row(new_row)
        return True
    except Exception as e:
        st.error(f"❌ บันทึกข้อมูลไม่สำเร็จ: {e}")
        return False

# ===== ฟังก์ชันค้นหาสินค้า =====
def find_item_by_barcode(sheet, barcode_id):
    """
    ค้นหาสินค้าจากรหัสบาร์โค้ด
    Return: dictionary ของข้อมูลสินค้า หรือ None ถ้าไม่เจอ
    """
    try:
        worksheet = sheet.worksheet("Inventory")
        all_records = worksheet.get_all_records()
        
        for record in all_records:
            if str(record['Barcode_ID']) == str(barcode_id):
                return record
        
        return None
    except Exception as e:
        st.error(f"❌ ค้นหาข้อมูลไม่สำเร็จ: {e}")
        return None

# ===== ฟังก์ชันอัปเดตสถานะสินค้าเป็น Sold =====
def mark_as_sold(sheet, barcode_id):
    """
    เปลี่ยนสถานะสินค้าจาก Available เป็น Sold
    และบันทึกวันที่ขาย
    """
    try:
        worksheet = sheet.worksheet("Inventory")
        
        # ค้นหาแถวที่ตรงกับ Barcode_ID
        cell = worksheet.find(str(barcode_id))
        
        if cell:
            row_num = cell.row
            
            # อัปเดตคอลัมน์ Status (คอลัมน์ 7) และ Sold_Date (คอลัมน์ 9)
            worksheet.update_cell(row_num, 7, "Sold")
            worksheet.update_cell(row_num, 9, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            return True
        else:
            st.error("❌ ไม่พบรหัสสินค้านี้ในระบบ")
            return False
            
    except Exception as e:
        st.error(f"❌ อัปเดตสถานะไม่สำเร็จ: {e}")
        return False

# ===== ฟังก์ชันโหลดข้อมูลทั้งหมด =====
def load_all_inventory(sheet):
    """
    โหลดข้อมูลสินค้าทั้งหมดจาก Google Sheets
    Return: DataFrame
    """
    try:
        worksheet = sheet.worksheet("Inventory")
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ โหลดข้อมูลไม่สำเร็จ: {e}")
        return pd.DataFrame()

# ===== CSS สำหรับปรับแต่งหน้าตา =====
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ===== MAIN APP =====
def main():
    st.title("👕 Thrift Shop POS System")
    st.markdown("### ระบบจัดการร้านเสื้อผ้ามือสอง")
    
    # เชื่อมต่อ Google Sheets
    sheet = connect_to_sheets()
    
    if sheet is None:
        st.stop()
    
    # สร้าง Sidebar สำหรับเลือกเมนู
    menu = st.sidebar.selectbox(
        "📋 เมนู",
        ["🏠 Dashboard", "📦 รับของเข้าสต็อก", "🛒 จุดขายสินค้า (POS)"]
    )
    
    # ===== หน้า Dashboard =====
    if menu == "🏠 Dashboard":
        st.header("📊 Dashboard & สรุปยอด")
        
        df = load_all_inventory(sheet)
        
        if not df.empty:
            # คำนวณสถิติ
            total_items = len(df)
            available_items = len(df[df['Status'] == 'Available'])
            sold_items = len(df[df['Status'] == 'Sold'])
            
            # คำนวณกำไร
            sold_df = df[df['Status'] == 'Sold'].copy()
            if not sold_df.empty:
                sold_df['Profit'] = sold_df['Price'] - sold_df['Cost']
                total_profit = sold_df['Profit'].sum()
            else:
                total_profit = 0
            
            # แสดงสถิติแบบ Metric Cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📦 สินค้าทั้งหมด", f"{total_items} ชิ้น")
            
            with col2:
                st.metric("✅ คงเหลือในสต็อก", f"{available_items} ชิ้น", delta=None, delta_color="normal")
            
            with col3:
                st.metric("💰 ขายแล้ว", f"{sold_items} ชิ้น", delta=None, delta_color="inverse")
            
            with col4:
                st.metric("💵 กำไรสะสม", f"฿{total_profit:,.2f}")
            
            st.markdown("---")
            
            # ตารางสินค้าคงเหลือ
            st.subheader("📋 รายการสินค้าคงเหลือ")
            
            available_df = df[df['Status'] == 'Available'].copy()
            
            if not available_df.empty:
                # ฟิลเตอร์
                col_filter1, col_filter2 = st.columns(2)
                
                with col_filter1:
                    brands = ['ทั้งหมด'] + sorted(available_df['Brand'].unique().tolist())
                    selected_brand = st.selectbox("🏷️ กรองตามแบรนด์", brands)
                
                with col_filter2:
                    sizes = ['ทั้งหมด'] + sorted(available_df['Size'].unique().tolist())
                    selected_size = st.selectbox("📏 กรองตามไซส์", sizes)
                
                # ใช้ฟิลเตอร์
                filtered_df = available_df.copy()
                if selected_brand != 'ทั้งหมด':
                    filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
                if selected_size != 'ทั้งหมด':
                    filtered_df = filtered_df[filtered_df['Size'] == selected_size]
                
                # แสดงตาราง
                st.dataframe(
                    filtered_df[['Barcode_ID', 'Item_Name', 'Brand', 'Size', 'Price']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("📭 ไม่มีสินค้าคงเหลือในสต็อก")
        else:
            st.warning("⚠️ ยังไม่มีข้อมูลในระบบ กรุณาเพิ่มสินค้าก่อน")
    
    # ===== หน้ารับของเข้าสต็อก =====
    elif menu == "📦 รับของเข้าสต็อก":
        st.header("📦 รับของเข้าสต็อก")
        
        with st.form("inventory_form", clear_on_submit=True):
            st.subheader("📝 กรอกข้อมูลสินค้า")
            
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("ชื่อสินค้า *", placeholder="เช่น เสื้อยืดสีขาว")
                brand = st.text_input("แบรนด์ *", placeholder="เช่น Uniqlo")
                size = st.selectbox("ไซส์ *", ["S", "M", "L", "XL", "XXL", "Free Size", "อื่นๆ"])
            
            with col2:
                cost = st.number_input("ต้นทุน (฿) *", min_value=0.0, step=1.0, format="%.2f")
                price = st.number_input("ราคาขาย (฿) *", min_value=0.0, step=1.0, format="%.2f")
            
            submitted = st.form_submit_button("✅ บันทึกสินค้า", use_container_width=True, type="primary")
            
            if submitted:
                # ตรวจสอบข้อมูล
                if not item_name or not brand:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
                elif cost <= 0 or price <= 0:
                    st.error("❌ ต้นทุนและราคาขายต้องมากกว่า 0")
                elif price < cost:
                    st.warning("⚠️ ราคาขายต่ำกว่าต้นทุน คุณจะขาดทุน!")
                    if st.button("ยืนยันบันทึกต่อ"):
                        pass
                else:
                    # สร้างรหัสบาร์โค้ด
                    barcode_id = generate_barcode_id()
                    
                    # บันทึกลง Google Sheets
                    with st.spinner("กำลังบันทึกข้อมูล..."):
                        success = add_inventory_item(
                            sheet, barcode_id, item_name, brand, 
                            size, cost, price
                        )
                    
                    if success:
                        st.success("✅ บันทึกสินค้าสำเร็จ!")
                        
                        # แสดงข้อมูลสินค้า
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>📋 ข้อมูลสินค้า</h3>
                            <p><strong>รหัสสินค้า:</strong> {barcode_id}</p>
                            <p><strong>ชื่อสินค้า:</strong> {item_name}</p>
                            <p><strong>แบรนด์:</strong> {brand} | <strong>ไซส์:</strong> {size}</p>
                            <p><strong>ต้นทุน:</strong> ฿{cost:.2f} | <strong>ราคาขาย:</strong> ฿{price:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # สร้างและแสดง QR Code
                        st.markdown("---")
                        st.subheader("📱 QR Code สำหรับพิมพ์แปะป้าย")
                        
                        qr_image = generate_qr_code(barcode_id)
                        
                        col_qr1, col_qr2 = st.columns([1, 2])
                        
                        with col_qr1:
                            st.image(qr_image, caption=f"รหัส: {barcode_id}", width=250)
                        
                        with col_qr2:
                            st.markdown(f"""
                            ### วิธีใช้งาน QR Code:
                            1. 📸 คลิกขวาที่ภาพ QR Code แล้วบันทึก
                            2. 🖨️ นำไปพิมพ์ด้วย Thermal Printer หรือ Printer ทั่วไป
                            3. ✂️ ตัดและแปะที่ป้ายเสื้อ
                            4. 📷 สแกนด้วยแอปเพื่อขายสินค้า
                            
                            **รหัสสินค้า:** `{barcode_id}`
                            """)
                            
                            # ปุ่มดาวน์โหลด QR Code
                            st.download_button(
                                label="💾 ดาวน์โหลด QR Code",
                                data=qr_image,
                                file_name=f"QR_{barcode_id}.png",
                                mime="image/png",
                                use_container_width=True
                            )
    
    # ===== หน้าจุดขายสินค้า (POS) =====
    elif menu == "🛒 จุดขายสินค้า (POS)":
        st.header("🛒 จุดขายสินค้า (POS)")
        
        # ช่องสำหรับสแกนหรือพิมพ์รหัส
        barcode_input = st.text_input(
            "🔍 สแกนหรือพิมพ์รหัสสินค้า",
            placeholder="กรอกรหัสแล้วกด Enter",
            key="barcode_scanner"
        )
        
        if barcode_input:
            with st.spinner("กำลังค้นหาสินค้า..."):
                item = find_item_by_barcode(sheet, barcode_input)
            
            if item:
                # ตรวจสอบสถานะสินค้า
                if item['Status'] == 'Sold':
                    st.error("❌ สินค้านี้ถูกขายไปแล้ว!")
                    st.info(f"📅 ขายเมื่อ: {item['Sold_Date']}")
                else:
                    # แสดงข้อมูลสินค้า
                    st.success("✅ พบสินค้าในระบบ!")
                    
                    col_item1, col_item2 = st.columns(2)
                    
                    with col_item1:
                        st.markdown(f"""
                        ### 📦 ข้อมูลสินค้า
                        - **รหัส:** {item['Barcode_ID']}
                        - **ชื่อ:** {item['Item_Name']}
                        - **แบรนด์:** {item['Brand']}
                        - **ไซส์:** {item['Size']}
                        """)
                    
                    with col_item2:
                        st.markdown(f"""
                        ### 💰 ข้อมูลราคา
                        - **ราคาขาย:** ฿{item['Price']:,.2f}
                        - **ต้นทุน:** ฿{item['Cost']:,.2f}
                        - **กำไร:** ฿{item['Price'] - item['Cost']:,.2f}
                        """)
                    
                    st.markdown("---")
                    
                    # ปุ่มยืนยันการขาย
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                    
                    with col_btn2:
                        if st.button("✅ ยืนยันการขาย", use_container_width=True, type="primary"):
                            with st.spinner("กำลังบันทึกการขาย..."):
                                success = mark_as_sold(sheet, barcode_input)
                            
                            if success:
                                st.success("🎉 ขายสินค้าสำเร็จ!")
                                st.balloons()
                                
                                # แสดงใบเสร็จ
                                st.markdown(f"""
                                <div class="success-box">
                                    <h3 style="text-align: center;">🧾 ใบเสร็จรับเงิน</h3>
                                    <p style="text-align: center;">Thrift Shop POS</p>
                                    <hr>
                                    <p><strong>สินค้า:</strong> {item['Item_Name']}</p>
                                    <p><strong>แบรนด์:</strong> {item['Brand']} ({item['Size']})</p>
                                    <p><strong>ราคา:</strong> ฿{item['Price']:,.2f}</p>
                                    <hr>
                                    <p style="text-align: center;"><strong>ขอบคุณที่ใช้บริการ!</strong></p>
                                    <p style="text-align: center; font-size: 12px;">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                time.sleep(2)
                                st.rerun()
            else:
                st.error("❌ ไม่พบรหัสสินค้านี้ในระบบ")
                st.info("💡 กรุณาตรวจสอบรหัสอีกครั้งหรือเพิ่มสินค้าในหน้า 'รับของเข้าสต็อก'")

# ===== เรียกใช้แอป =====
if __name__ == "__main__":
    main()

"""
pages/edit_product.py — Standalone edit page for inventory items.
"""

import streamlit as st
from src.database.inventory import find_item_by_barcode, update_inventory_item
from src.components.ui_helpers import render_section, render_empty_state, render_divider
from src.config import SIZE_OPTIONS, CONDITION_OPTIONS


def render(sheet):
    render_section("✏️ แก้ไขข้อมูลสินค้า")

    # Input for Barcode ID
    st.markdown("ระบุ รหัสสินค้า (Barcode ID) ที่ต้องการแก้ไข")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_id = st.text_input("รหัสสินค้า", placeholder="เช่น UNIQLO-SH-001", label_visibility="collapsed")
    with col2:
        search_btn = st.button("ค้นหา", use_container_width=True)

    # Use session state to remember the searched barcode
    if search_btn and search_id:
        st.session_state["edit_barcode_id"] = search_id.strip()

    barcode_to_edit = st.session_state.get("edit_barcode_id", "")

    if barcode_to_edit:
        render_divider()
        item_data = find_item_by_barcode(sheet, barcode_to_edit)
        
        if not item_data:
            st.error(f"❌ ไม่พบข้อมูลสินค้าสำหรับรหัส '{barcode_to_edit}'")
            return

        st.markdown(f"**กำลงแก้ไข:** `{barcode_to_edit}` - {item_data.get('Item_Name', '')}")
        
        with st.form(key=f"edit_form_{barcode_to_edit}"):
            st.markdown('### 📝 ข้อมูลทั่วไป')
            
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("ชื่อสินค้า", value=str(item_data.get("Item_Name", "")))
                new_brand = st.text_input("แบรนด์", value=str(item_data.get("Brand", "")))
                
                # Safe index for Size
                current_size = str(item_data.get("Size_Label", ""))
                size_index = SIZE_OPTIONS.index(current_size) if current_size in SIZE_OPTIONS else 0
                new_size = st.selectbox("ไซส์", SIZE_OPTIONS, index=size_index)

            with c2:
                # Safe index for Condition
                current_cond = str(item_data.get("Condition", ""))
                cond_index = CONDITION_OPTIONS.index(current_cond) if current_cond in CONDITION_OPTIONS else 0
                new_cond = st.selectbox("สภาพ", CONDITION_OPTIONS, index=cond_index)
                
                new_color = st.text_input("สี", value=str(item_data.get("Color", "")))
                new_pattern = st.text_input("ลวดลาย", value=str(item_data.get("Pattern", "")))

            new_material = st.text_input("วัสดุ/ผ้า", value=str(item_data.get("Material", "")))
            
            st.markdown('### 💰 ราคา')
            c3, c4 = st.columns(2)
            with c3:
                new_cost = st.number_input("ต้นทุน", value=float(item_data.get("Cost", 0)), step=1.0)
            with c4:
                new_price = st.number_input("ราคาขาย", value=float(item_data.get("Price", 0)), step=1.0)
                
            submit_button = st.form_submit_button(label="💾 บันทึกการแก้ไข", type="primary", use_container_width=True)
            
            if submit_button:
                if not new_name:
                    st.error("❌ กรุณากรอกชื่อสินค้า")
                elif new_cost < 0 or new_price < 0:
                    st.error("❌ ราคาหรือต้นทุนติดลบไม่ได้")
                else:
                    with st.spinner("⏳ กำลังบันทึก..."):
                        success = update_inventory_item(
                            sheet=sheet,
                            barcode_id=barcode_to_edit,
                            item_name=new_name,
                            brand=new_brand,
                            size_label=new_size,
                            condition=new_cond,
                            color=new_color,
                            pattern=new_pattern,
                            material=new_material,
                            cost=new_cost,
                            price=new_price
                        )
                        
                    if success:
                        st.success("🎉 อัปเดตข้อมูลสำเร็จ!")
                        st.cache_data.clear()
                        # Optional: st.rerun() if you want to immediately flush state

"""
pages/edit_product.py — Standalone edit page for inventory items.
Supports: edit fields, view/delete/add photos via Cloudinary.
"""

import json
import streamlit as st
from src.database.inventory import find_item_by_barcode, update_inventory_item
from src.components.ui_helpers import render_section, render_empty_state, render_divider
from src.config import SIZE_OPTIONS, CONDITION_OPTIONS
from src.services.cloudinary_images import upload_image as cld_upload, delete_image as cld_delete, get_thumbnail_url


def _parse_photos(photo_field: str) -> list:
    """Parse Photo column: handles JSON list (new) or legacy base64/URL (old)."""
    if not photo_field or str(photo_field).strip() in ("", "0", "None", "nan"):
        return []
    s = str(photo_field).strip()
    if s.startswith("["):
        try:
            urls = json.loads(s)
            return [u for u in urls if u]
        except Exception:
            return []
    # Legacy single value (base64 or old URL)
    return [s]


def render(sheet):
    render_section("✏️ แก้ไขข้อมูลสินค้า")

    col1, col2 = st.columns([3, 1])
    with col1:
        search_id = st.text_input("รหัสสินค้า", placeholder="เช่น UNIQLO-SH-001", label_visibility="collapsed")
    with col2:
        search_btn = st.button("ค้นหา", use_container_width=True)

    if search_btn and search_id:
        st.session_state["edit_barcode_id"] = search_id.strip()

    barcode_to_edit = st.session_state.get("edit_barcode_id", "")
    
    if not barcode_to_edit:
        render_empty_state("✏️", "กรอกรหัสสินค้าแล้วกด 'ค้นหา' เพื่อแก้ไข")
        return

    render_divider()
    item_data = find_item_by_barcode(sheet, barcode_to_edit)
    
    if not item_data:
        st.error(f"❌ ไม่พบข้อมูลสินค้าสำหรับรหัส '{barcode_to_edit}'")
        return

    st.markdown(f"**กำลังแก้ไข:** `{barcode_to_edit}` — {item_data.get('Item_Name', '')}")
    
    # ===== Main form =====
    with st.form(key=f"edit_form_{barcode_to_edit}"):
        st.markdown('### 📝 ข้อมูลทั่วไป')
        
        c1, c2 = st.columns(2)
        with c1:
            new_name  = st.text_input("ชื่อสินค้า", value=str(item_data.get("Item_Name", "")))
            new_brand = st.text_input("แบรนด์",    value=str(item_data.get("Brand", "")))
            current_size = str(item_data.get("Size_Label", ""))
            size_index   = SIZE_OPTIONS.index(current_size) if current_size in SIZE_OPTIONS else 0
            new_size     = st.selectbox("ไซส์", SIZE_OPTIONS, index=size_index)
        with c2:
            current_cond = str(item_data.get("Condition", ""))
            cond_index   = CONDITION_OPTIONS.index(current_cond) if current_cond in CONDITION_OPTIONS else 0
            new_cond     = st.selectbox("สภาพ",   CONDITION_OPTIONS, index=cond_index)
            new_color    = st.text_input("สี",     value=str(item_data.get("Color", "")))
            new_pattern  = st.text_input("ลวดลาย", value=str(item_data.get("Pattern", "")))

        new_material = st.text_input("วัสดุ/ผ้า", value=str(item_data.get("Material", "")))
        
        st.markdown('### 💰 ราคา')
        c3, c4 = st.columns(2)
        with c3:
            new_cost  = st.number_input("ต้นทุน",    value=float(item_data.get("Cost", 0)), step=1.0)
        with c4:
            new_price = st.number_input("ราคาขาย", value=float(item_data.get("Price", 0)), step=1.0)

        st.markdown('### 📸 เพิ่มรูปสินค้า (อัปโหลดไปยัง Cloudinary)')
        new_files = st.file_uploader(
            "รูปเพิ่มเติม", type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            help="เลือกได้หลายรูป — จะถูกเพิ่มต่อจากรูปเดิม",
            label_visibility="collapsed",
        )
        if new_files:
            cols_prev = st.columns(min(len(new_files), 3))
            for i, f in enumerate(new_files):
                with cols_prev[i % 3]:
                    st.image(f, caption=f"ใหม่ {i+1}", use_container_width=True)

        submit_button = st.form_submit_button(label="💾 บันทึกการแก้ไข", type="primary", use_container_width=True)
        
        if submit_button:
            if not new_name:
                st.error("❌ กรุณากรอกชื่อสินค้า")
            else:
                # Load existing URLs
                existing_urls = _parse_photos(str(item_data.get("Photo", "")))
                
                # Upload new files
                new_urls = []
                if new_files:
                    prog = st.progress(0, text="กำลังอัปโหลดรูป...")
                    for idx, f in enumerate(new_files):
                        next_idx = len(existing_urls) + idx + 1
                        url = cld_upload(f, barcode_to_edit, photo_index=next_idx)
                        if url:
                            new_urls.append(url)
                        prog.progress((idx + 1) / len(new_files))
                    prog.empty()

                all_urls = existing_urls + new_urls
                final_photo = json.dumps(all_urls) if all_urls else ""

                with st.spinner("⏳ กำลังบันทึก..."):
                    success = update_inventory_item(
                        sheet=sheet, barcode_id=barcode_to_edit,
                        item_name=new_name, brand=new_brand,
                        size_label=new_size, condition=new_cond,
                        color=new_color, pattern=new_pattern,
                        material=new_material, cost=new_cost,
                        price=new_price, photo_b64=final_photo,
                    )
                    
                if success:
                    st.success(f"🎉 อัปเดตสำเร็จ! มีรูป {len(all_urls)} รูป")
                    st.cache_data.clear()

    # ===== Photo Manager (outside form) =====
    render_divider()
    st.markdown("### 🗂️ จัดการรูปสินค้าปัจจุบัน")
    
    current_urls = _parse_photos(str(item_data.get("Photo", "")))
    
    if not current_urls:
        st.info("ยังไม่มีรูปสินค้า — อัปโหลดรูปด้านบนในฟอร์ม")
    else:
        st.caption(f"{len(current_urls)} รูป — กดปุ่ม '🗑️ ลบ' เพื่อลบรูปนั้น")
        cols = st.columns(min(len(current_urls), 3))
        urls_to_keep = list(current_urls)
        
        for i, url in enumerate(current_urls):
            with cols[i % 3]:
                # Detect legacy base64
                if url.startswith("http"):
                    thumb = get_thumbnail_url(url, width=300)
                    st.image(thumb, caption=f"รูป {i+1}", use_container_width=True)
                else:
                    # Legacy base64 — try to decode and show
                    try:
                        import base64
                        b = base64.b64decode(url)
                        st.image(b, caption=f"รูป {i+1} (เก่า)", use_container_width=True)
                    except Exception:
                        st.write(f"รูป {i+1} (ไม่สามารถแสดงได้)")
                
                if st.button(f"🗑️ ลบรูป {i+1}", key=f"del_{barcode_to_edit}_{i}"):
                    # Delete from Cloudinary if it's a Cloudinary URL
                    if "cloudinary.com" in url:
                        cld_delete(barcode_to_edit, i + 1)
                    urls_to_keep = [u for j, u in enumerate(current_urls) if j != i]
                    new_photo_val = json.dumps(urls_to_keep) if urls_to_keep else ""
                    with st.spinner("กำลังบันทึก..."):
                        update_inventory_item(
                            sheet=sheet, barcode_id=barcode_to_edit,
                            item_name=str(item_data.get("Item_Name", "")),
                            brand=str(item_data.get("Brand", "")),
                            size_label=str(item_data.get("Size_Label", "")),
                            condition=str(item_data.get("Condition", "")),
                            color=str(item_data.get("Color", "")),
                            pattern=str(item_data.get("Pattern", "")),
                            material=str(item_data.get("Material", "")),
                            cost=float(item_data.get("Cost", 0)),
                            price=float(item_data.get("Price", 0)),
                            photo_b64=new_photo_val,
                        )
                    st.cache_data.clear()
                    st.rerun()

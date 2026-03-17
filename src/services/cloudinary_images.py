# -*- coding: utf-8 -*-
"""
services/cloudinary_images.py — Upload & manage product images via Cloudinary.
"""

import cloudinary
import cloudinary.uploader
import streamlit as st
from io import BytesIO
from PIL import Image

def _configure() -> bool:
    """
    Configure Cloudinary from st.secrets every call — safe because
    Cloudinary.config() is idempotent and secrets are always available.
    """
    try:
        cld = st.secrets["cloudinary"]
        cloudinary.config(
            cloud_name=cld["cloud_name"],
            api_key=str(cld["api_key"]),
            api_secret=cld["api_secret"],
            secure=True
        )
        return True
    except KeyError:
        st.error("⚙️ ไม่พบ [cloudinary] ใน .streamlit/secrets.toml กรุณาตรวจสอบ")
        return False
    except Exception as e:
        st.error(f"❌ ตั้งค่า Cloudinary ไม่สำเร็จ: {e}")
        return False


def upload_image(uploaded_file, barcode_id: str, photo_index: int = 1) -> str:
    """
    อัปโหลดรูปไปยัง Cloudinary.
    คืน URL ของรูปที่ upload สำเร็จ หรือ "" ถ้าไม่สำเร็จ
    """
    if not _configure():
        return ""
    try:
        # Resize + convert to RGB
        img = Image.open(uploaded_file)
        img.thumbnail((800, 800), Image.LANCZOS)
        if img.mode in ("RGBA", "P", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            mask = img.split()[-1] if img.mode in ("RGBA", "LA") else None
            bg.paste(img, mask=mask)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buf = BytesIO()
        img.save(buf, format="JPEG", quality=82, optimize=True)
        buf.seek(0)

        public_id = f"thrift-pos/{barcode_id}/photo_{photo_index}"
        result = cloudinary.uploader.upload(
            buf,
            public_id=public_id,
            overwrite=True,
            resource_type="image",
            format="jpg"
        )
        url = result.get("secure_url", "")
        if url:
            st.success(f"✅ อัปโหลดรูปสำเร็จ: [ดูรูป]({url})")
        return url
    except Exception as e:
        st.error(f"❌ อัปโหลดรูปไม่สำเร็จ: {e}")
        return ""


def delete_image(barcode_id: str, photo_index: int) -> bool:
    """ลบรูปออกจาก Cloudinary โดยใช้ public_id."""
    if not _configure():
        return False
    try:
        public_id = f"thrift-pos/{barcode_id}/photo_{photo_index}"
        cloudinary.uploader.destroy(public_id)
        return True
    except Exception as e:
        st.warning(f"⚠️ ลบรูปจาก Cloudinary ไม่สำเร็จ: {e}")
        return False


def get_thumbnail_url(url: str, width: int = 300) -> str:
    """แปลง Cloudinary URL ให้โหลดเป็น thumbnail ขนาดเล็กอัตโนมัติ."""
    if not url or "cloudinary.com" not in url:
        return url
    return url.replace("/upload/", f"/upload/w_{width},h_{width},c_fill,q_auto/")

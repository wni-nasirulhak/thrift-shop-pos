"""
services/images.py — Image processing and storage.

Two storage backends are supported:
  1. Base64 thumbnail  → stored directly in Google Sheets (Photo column)
                         Best for: small shops, no Drive setup needed
  2. Google Drive      → full-resolution images stored in Drive, URLs in Sheet
                         Best for: production use, unlimited storage

Use `compress_to_base64()` for quick setup.
Use `DriveImageService` when Drive is authorized (token.pickle exists).
"""

import base64
import os
import pickle
import streamlit as st
from io import BytesIO
from PIL import Image
from src.config import (
    IMAGE_THUMB_SIZE_PX, IMAGE_THUMB_QUALITY,
    IMAGE_MAX_SIZE_PX, IMAGE_MAX_PER_ITEM,
    DRIVE_TOKEN_PATH, SHEET_PRODUCT_IMAGES,
)


# ===== Base64 helpers =====

def compress_to_base64(uploaded_file, max_size: int = IMAGE_THUMB_SIZE_PX, quality: int = IMAGE_THUMB_QUALITY) -> str:
    """
    อ่านไฟล์ที่อัปโหลด, ย่อขนาด, แปลงเป็น base64 string.
    คืน "" ถ้าเกิดข้อผิดพลาด
    """
    try:
        img = Image.open(uploaded_file)
        img.thumbnail((max_size, max_size), Image.LANCZOS)

        # แปลง transparent modes → RGB
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
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        st.warning(f"⚠️ แปลงรูปไม่สำเร็จ: {e}")
        return ""


def decode_base64_to_bytes(b64_data) -> bytes | None:
    """
    แปลง base64 string กลับเป็น bytes สำหรับ st.image().
    คืน None ถ้าข้อมูลไม่ถูกต้อง (รวมถึง 0, '', 'None' จาก gspread)
    """
    if not b64_data:
        return None
    s = str(b64_data).strip()
    if s in ("", "0", "None", "nan", "#N/A", "FALSE", "false"):
        return None
    try:
        return base64.b64decode(s)
    except Exception:
        return None


def estimate_size_kb(b64_str: str) -> float:
    """ประมาณขนาดไฟล์จาก base64 string (KB)."""
    return len(b64_str) * 3 / 4 / 1024


# ===== Google Drive backend =====

class DriveImageService:
    """
    จัดการรูปภาพผ่าน Google Drive API (OAuth 2.0).
    ต้องรัน tools/authorize_drive.py ก่อนใช้งานครั้งแรก
    """

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    def __init__(self, token_path: str = DRIVE_TOKEN_PATH):
        self.token_path = token_path
        self.service = None
        self._connect()

    def is_ready(self) -> bool:
        return self.service is not None

    def _connect(self):
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            if not os.path.exists(self.token_path):
                st.warning("⚠️ ไม่พบ token.pickle — กรุณารัน tools/authorize_drive.py ก่อน")
                return

            with open(self.token_path, "rb") as f:
                creds = pickle.load(f)

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(self.token_path, "wb") as f:
                    pickle.dump(creds, f)

            if not creds or not creds.valid:
                st.error("❌ Drive token ไม่ถูกต้อง — กรุณา authorize ใหม่")
                return

            self.service = build("drive", "v3", credentials=creds)
        except Exception as e:
            st.error(f"❌ เชื่อมต่อ Google Drive ไม่สำเร็จ: {e}")

    def upload_image(self, image_bytes: bytes, filename: str, folder_id: str) -> str | None:
        """อัปโหลดรูปไป Drive, คืน direct URL."""
        if not self.is_ready():
            return None
        try:
            from googleapiclient.http import MediaIoBaseUpload

            resized = self._resize(image_bytes)
            if not resized:
                return None

            file_meta = {"name": filename, "parents": [folder_id]}
            media = MediaIoBaseUpload(resized, mimetype="image/jpeg", resumable=True)
            file = self.service.files().create(body=file_meta, media_body=media, fields="id").execute()
            file_id = file.get("id")

            self.service.permissions().create(
                fileId=file_id,
                body={"type": "anyone", "role": "reader"},
            ).execute()

            return f"https://drive.google.com/uc?export=view&id={file_id}"
        except Exception as e:
            st.error(f"❌ อัปโหลดรูปไม่สำเร็จ: {e}")
            return None

    def create_product_folder(self, barcode_id: str, parent_folder_id: str | None = None) -> str | None:
        """สร้างโฟลเดอร์สินค้าใน Drive. คืน folder_id."""
        if not self.is_ready():
            return None
        try:
            from datetime import datetime as dt
            month_label = dt.now().strftime("%Y-%m")

            month_folder_id = self._get_or_create_folder(month_label, parent_folder_id)
            if not month_folder_id:
                return None

            return self._get_or_create_folder(barcode_id, month_folder_id)
        except Exception as e:
            st.error(f"❌ สร้างโฟลเดอร์ไม่สำเร็จ: {e}")
            return None

    def upload_product_images(self, barcode_id: str, files: list, parent_folder_id: str | None = None) -> dict | None:
        """
        อัปโหลดรูปสินค้าหลายรูป (สูงสุด IMAGE_MAX_PER_ITEM รูป).
        คืน {'urls': {image_1: url, ...}, 'folder_id': str}
        """
        if not self.is_ready():
            return None

        folder_id = self.create_product_folder(barcode_id, parent_folder_id)
        if not folder_id:
            return None

        urls = {}
        for idx, f in enumerate(files[:IMAGE_MAX_PER_ITEM], 1):
            if f is None:
                continue
            img_bytes = f.read()
            url = self.upload_image(img_bytes, f"{idx}_{f.name}", folder_id)
            if url:
                urls[f"image_{idx}"] = url
            f.seek(0)

        return {"urls": urls, "folder_id": folder_id}

    # --- Private ---

    def _resize(self, image_bytes: bytes, max_size: int = IMAGE_MAX_SIZE_PX) -> BytesIO | None:
        try:
            img = Image.open(BytesIO(image_bytes))
            if img.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
                img = bg
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.LANCZOS)
            out = BytesIO()
            img.save(out, format="JPEG", quality=85, optimize=True)
            out.seek(0)
            return out
        except Exception as e:
            st.error(f"❌ Resize รูปไม่สำเร็จ: {e}")
            return None

    def _get_or_create_folder(self, name: str, parent_id: str | None) -> str | None:
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        res = self.service.files().list(q=query, spaces="drive", fields="files(id)").execute()
        files = res.get("files", [])
        if files:
            return files[0]["id"]
        meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            meta["parents"] = [parent_id]
        folder = self.service.files().create(body=meta, fields="id").execute()
        return folder.get("id")


# ===== Drive sheet helpers =====

def save_drive_image_urls(sheet, barcode_id: str, urls: dict, folder_id: str, uploaded_by: str = "Admin") -> bool:
    """บันทึก Drive URLs ลง Product_Images sheet."""
    try:
        ws = sheet.worksheet(SHEET_PRODUCT_IMAGES)
        try:
            if ws.find(barcode_id):
                st.warning(f"⚠️ {barcode_id} มีรูปอยู่แล้วใน Product_Images")
                return False
        except Exception:
            pass

        from datetime import datetime as dt
        row = [
            barcode_id,
            urls.get("image_1", ""),
            urls.get("image_2", ""),
            urls.get("image_3", ""),
            urls.get("image_4", ""),
            urls.get("image_5", ""),
            "1",
            dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            folder_id,
            uploaded_by,
            "",
        ]
        ws.append_row(row)
        return True
    except Exception as e:
        st.error(f"❌ บันทึก Drive URLs ไม่สำเร็จ: {e}")
        return False


def load_drive_image_urls(sheet, barcode_id: str) -> dict | None:
    """โหลด Drive URLs จาก Product_Images sheet."""
    try:
        ws = sheet.worksheet(SHEET_PRODUCT_IMAGES)
        records = ws.get_all_records()
        for rec in records:
            if str(rec.get("Barcode_ID", "")) == str(barcode_id):
                return {
                    "image_1":    rec.get("Image_1_URL", ""),
                    "image_2":    rec.get("Image_2_URL", ""),
                    "image_3":    rec.get("Image_3_URL", ""),
                    "image_4":    rec.get("Image_4_URL", ""),
                    "image_5":    rec.get("Image_5_URL", ""),
                    "main_image": int(rec.get("Main_Image", 1) or 1),
                    "folder_id":  rec.get("Drive_Folder_ID", ""),
                }
        return None
    except Exception as e:
        st.error(f"❌ โหลดรูป Drive ไม่สำเร็จ: {e}")
        return None

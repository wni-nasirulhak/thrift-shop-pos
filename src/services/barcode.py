"""
services/barcode.py — Barcode generation and QR code creation.
"""

from datetime import datetime
from io import BytesIO
import qrcode
from src.config import BARCODE_PAD_DIGITS


def generate_barcode_id(brand_code: str, category_code: str, sheet) -> str:
    """
    สร้าง Barcode ID อัตโนมัติ รูปแบบ: {BRAND}-{CAT}-{SEQ}
    ตัวอย่าง: UNIQLO-SH-004

    ถ้าอ่าน sheet ไม่ได้ จะใช้ timestamp แทน sequence
    """
    try:
        from src.config import SHEET_INVENTORY
        ws = sheet.worksheet(SHEET_INVENTORY)
        records = ws.get_all_records()
        prefix = f"{brand_code}-{category_code}"
        count = sum(
            1 for r in records
            if str(r.get("Barcode_ID", "")).startswith(prefix)
        )
        seq = str(count + 1).zfill(BARCODE_PAD_DIGITS)
        return f"{prefix}-{seq}"
    except Exception:
        ts = datetime.now().strftime("%H%M%S")
        return f"{brand_code}-{category_code}-{ts}"


def generate_qr_bytes(data: str, box_size: int = 10) -> bytes | None:
    """
    สร้าง QR Code จาก string และคืนค่าเป็น PNG bytes.
    (ใช้ bytes แทน BytesIO เพื่อให้ st.image() และ st.download_button() ใช้ร่วมกันได้)
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        # qrcode PIL image — ใช้ .get_image() ถ้ามี ไม่งั้นใช้ตรง
        pil_img = img.get_image() if hasattr(img, "get_image") else img
        if hasattr(pil_img, "save"):
            pil_img.save(buf, format="PNG")
        else:
            img.save(buf, format="PNG")

        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        return None

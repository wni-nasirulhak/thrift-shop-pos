"""
config.py — Constants, settings, and sheet schema definitions.
Edit this file to change app-wide settings without touching business logic.
"""

# ===== App Info =====
APP_VERSION = "4.0"
APP_TITLE = "Thrift Shop POS"
APP_ICON = "👕"

# ===== Google Sheets — Worksheet Names =====
SHEET_INVENTORY        = "Inventory"
SHEET_CATEGORIES       = "Categories"
SHEET_BRANDS           = "Brands"
SHEET_SALES            = "Sales"
SHEET_CUSTOMERS        = "Customers"
SHEET_SHIPPING         = "Shipping"
SHEET_MEASUREMENTS     = {
    "CAT-SH": "Measurements_Shirts",
    "CAT-PA": "Measurements_Pants",
    "CAT-FW": "Measurements_Shoes",
}
SHEET_PRODUCT_IMAGES   = "Product_Images"

# ===== Inventory — Column index (0-based) =====
# Used when calling update_cell; keep in sync with sheet header row.
INV_COL_STATUS = 13   # Column M (1-based = 13)

# ===== Image settings =====
IMAGE_MAX_SIZE_PX   = 1200   # Max width/height for Drive uploads
IMAGE_THUMB_SIZE_PX = 400    # Max width/height for base64 thumbnails
IMAGE_THUMB_QUALITY = 55     # JPEG quality for thumbnails (lower = smaller file)
IMAGE_MAX_PER_ITEM  = 5      # Max photos per product

# Google Drive OAuth token path (relative to project root)
DRIVE_TOKEN_PATH    = "token.pickle"
DRIVE_CREDENTIALS   = "credentials.json"

# ===== Barcode =====
BARCODE_PAD_DIGITS = 3   # e.g. 001, 002 … 999

# ===== Size options =====
SIZE_OPTIONS = ["XS", "S", "M", "L", "XL", "XXL", "Free Size", "ไม่ระบุ"]

CONDITION_OPTIONS = [
    "⭐⭐⭐⭐⭐ Like New",
    "⭐⭐⭐⭐ Excellent",
    "⭐⭐⭐ Good",
    "⭐⭐ Fair",
    "⭐ Vintage",
]

PAYMENT_OPTIONS = ["💵 Cash", "📱 QR Code", "💳 Card"]

# ===== Measurement fields per category =====
# Extend this dict when new categories are added.
MEASUREMENT_FIELDS = {
    "CAT-SH": {
        "numeric": ["chest", "length", "sleeve", "shoulder"],
        "select": {
            "collar_type": ["คอกลม", "คอวี", "คอปก", "คอเต่า", "อื่นๆ"],
            "fit":         ["Regular", "Slim", "Oversized"],
        },
        "labels": {
            "chest":   "รอบอก",
            "length":  "ความยาว",
            "sleeve":  "แขน",
            "shoulder":"ไหล่",
        },
    },
    "CAT-PA": {
        "numeric": ["waist", "hip", "length", "inseam", "leg_opening", "rise", "thigh"],
        "select": {
            "fit": ["Skinny", "Regular", "Wide", "Straight"],
        },
        "labels": {
            "waist":       "รอบเอว",
            "hip":         "รอบสะโพก",
            "length":      "ความยาว",
            "inseam":      "ขาใน",
            "leg_opening": "ปลายขา",
            "rise":        "ความสูงเป้า",
            "thigh":       "รอบขาบน",
        },
    },
    "CAT-FW": {
        "text":    ["size_us", "size_eu", "size_uk", "size_jp", "condition_sole"],
        "numeric": ["insole_length", "heel_height"],
        "select": {
            "width": ["Normal", "Wide", "Narrow"],
        },
        "labels": {
            "size_us":       "🇺🇸 US Size",
            "size_eu":       "🇪🇺 EU Size",
            "size_uk":       "🇬🇧 UK Size",
            "size_jp":       "🇯🇵 JP Size",
            "insole_length": "พื้นใน (ซม.)",
            "heel_height":   "ส้นสูง (ซม.)",
            "condition_sole":"สภาพพื้น",
        },
    },
}

# ===== Cache TTL (seconds) =====
CACHE_TTL_CATALOG   = 60    # Categories / Brands
CACHE_TTL_INVENTORY = 30    # Inventory list

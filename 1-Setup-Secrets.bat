@echo off
chcp 65001 >nul
title สร้าง secrets.toml อัตโนมัติ
color 0A

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   🔐 สคริปต์สร้าง secrets.toml อัตโนมัติ        ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ Python! กรุณาติดตั้ง Python ก่อน
    echo    ดาวน์โหลดที่: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ พบ Python แล้ว
echo.
echo 🚀 กำลังรันสคริปต์...
echo.

python setup_secrets.py

echo.
pause

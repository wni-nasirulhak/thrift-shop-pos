@echo off
chcp 65001 >nul
title ติดตั้ง Dependencies
color 0B

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   📦 ติดตั้ง Libraries ที่จำเป็น                 ║
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
echo 🚀 กำลังติดตั้ง libraries จาก requirements.txt...
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ ติดตั้งไม่สำเร็จ! กรุณาตรวจสอบ error ด้านบน
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   ✅ ติดตั้งสำเร็จ!                               ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo ✨ พร้อมใช้งานแล้ว! ขั้นตอนต่อไป:
echo    1. ดับเบิลคลิก "1-Setup-Secrets.bat" เพื่อตั้งค่า
echo    2. ดับเบิลคลิก "3-Run-App.bat" เพื่อรันแอป
echo.
pause

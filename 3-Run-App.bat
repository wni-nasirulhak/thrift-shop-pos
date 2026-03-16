@echo off
chcp 65001 >nul
title Thrift Shop POS - Running...
color 0E

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   🚀 กำลังเปิด Thrift Shop POS...                ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ Python! กรุณาติดตั้ง Python ก่อน
    pause
    exit /b 1
)

REM ตรวจสอบว่ามีไฟล์ secrets.toml หรือไม่
if not exist ".streamlit\secrets.toml" (
    echo ❌ ไม่พบไฟล์ secrets.toml!
    echo.
    echo 💡 กรุณารันไฟล์ "1-Setup-Secrets.bat" ก่อน
    echo    เพื่อสร้างไฟล์ตั้งค่าการเชื่อมต่อ Google Sheets
    echo.
    pause
    exit /b 1
)

echo ✅ พบไฟล์ตั้งค่าแล้ว
echo.
echo 🌐 แอปจะเปิดในเบราว์เซอร์อัตโนมัติ...
echo    URL: http://localhost:8501
echo.
echo ⚠️ อย่าปิดหน้าต่างนี้! (แอปจะหยุดทำงาน)
echo    ต้องการหยุด: กด Ctrl+C
echo.
echo ════════════════════════════════════════════════════
echo.

streamlit run app.py

pause

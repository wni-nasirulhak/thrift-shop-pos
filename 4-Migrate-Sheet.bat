@echo off
chcp 65001 >nul
title อัปเดต Google Sheet Structure
color 0D

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   🔄 อัปเดต Google Sheet Structure v2.0         ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ Python! กรุณาติดตั้ง Python ก่อน
    pause
    exit /b 1
)

echo ✅ พบ Python แล้ว
echo.

REM ติดตั้ง toml library (สำหรับอ่าน secrets.toml)
echo 📦 กำลังติดตั้ง toml library...
pip install toml -q

echo.
echo 🚀 กำลังรันสคริปต์ย้ายข้อมูล...
echo.
echo ⚠️ สคริปต์นี้จะ:
echo    1. อ่านข้อมูลเดิมจากชีท Inventory
echo    2. สำรองข้อมูลไปชีท Inventory_Backup
echo    3. อัปเดต header ให้มี 14 คอลัมน์
echo    4. ย้ายข้อมูลเดิมไปคอลัมน์ใหม่
echo.

pause

python migrate_sheet.py

echo.
pause

@echo off
chcp 65001 >nul
title Thrift Shop POS

echo.
echo  ==========================================
echo   Thrift Shop POS - Starting...
echo  ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found. Please install Python 3.10+
    pause & exit /b 1
)

if not exist ".streamlit\secrets.toml" (
    echo  ERROR: .streamlit\secrets.toml not found
    echo  Please create it following secrets.toml.example
    pause & exit /b 1
)

echo  URL: http://localhost:8501
echo  Press Ctrl+C to stop
echo.

streamlit run app.py

pause

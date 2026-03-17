@echo off
chcp 65001 >nul
title Install Dependencies

echo  Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo  Done! Run scripts\run.bat to start the app.
pause

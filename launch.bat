@echo off
title Face Recognition App Launcher
echo.
echo 🎯 Starting Face Recognition App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Launch the Python script
python launcher.py

echo.
echo Press any key to exit...
pause >nul

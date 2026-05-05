@echo off
REM Weather App - Complete Startup (Backend + Frontend)
REM This script starts both Flask backend and frontend automatically

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo    Weather App - Complete Startup
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Setup Backend
cd backend

if not exist venv (
    echo [*] Creating Python virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -q -r requirements.txt >nul 2>&1
echo [OK] Dependencies installed
echo.

REM Start Backend in new window
echo [*] Starting Flask Backend...
start "Flask Backend - http://localhost:5000" cmd /k "cd backend && venv\Scripts\activate.bat && python app.py"

REM Wait for backend to start
timeout /t 2 >nul

REM Start Frontend in new window
echo [*] Starting Frontend Server...
cd ..
cd frontend
start "Frontend Server - http://localhost:8000" cmd /k "python -m http.server 8000"

echo.
echo ==========================================
echo    Startup Complete!
echo ==========================================
echo.
echo [OK] Backend:  http://localhost:5000
echo [OK] Frontend: http://localhost:8000
echo.
echo Opening browser...
echo.

REM Open browser
timeout /t 2 >nul
start http://localhost:8000

echo.
echo Press any key to close this window...
echo (Backend and Frontend will continue running)
echo.
pause

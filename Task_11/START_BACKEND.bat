@echo off
REM Weather App - Simple Startup

echo.
echo ========================================
echo   Weather App Startup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo [OK] Python installed
echo.

REM Setup and run backend
cd backend
if not exist venv (
    echo [*] Creating virtual environment...
    python -m venv venv
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo   Starting Flask Backend
echo ========================================
echo   URL: http://localhost:5000
echo.
echo   To stop: Press CTRL+C
echo ========================================
echo.

python app.py

pause

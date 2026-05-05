@echo off
REM Weather App - Start Script for Windows

echo.
echo ====================================
echo   Weather App - Startup Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Python is installed
echo.

REM Setup backend
echo [STEP 1] Setting up Flask backend...
cd backend

REM Check if venv exists
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)

REM Start Flask app in a new window
echo [INFO] Starting Flask backend on http://localhost:5000...
start cmd /k python app.py

cd ..

REM Setup frontend
echo [STEP 2] Starting frontend server...
echo [INFO] Frontend will be available at http://localhost:8000
echo.

cd frontend

REM Start simple HTTP server
start cmd /k python -m http.server 8000

cd ..

echo.
echo ====================================
echo   Startup Complete!
echo ====================================
echo.
echo [SUCCESS] Both servers are starting:
echo   - Backend:  http://localhost:5000
echo   - Frontend: http://localhost:8000
echo.
echo Open http://localhost:8000 in your browser
echo.
echo Press any key to exit this window (servers will continue running)
pause

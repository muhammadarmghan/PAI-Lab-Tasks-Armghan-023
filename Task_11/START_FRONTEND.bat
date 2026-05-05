@echo off
REM Weather App - Frontend Startup

echo.
echo ========================================
echo   Weather App - Frontend Server
echo ========================================
echo.

cd frontend

echo [*] Starting HTTP Server...
echo.
echo ========================================
echo   Frontend URL: http://localhost:8000
echo.
echo   To stop: Press CTRL+C
echo ========================================
echo.

python -m http.server 8000

pause

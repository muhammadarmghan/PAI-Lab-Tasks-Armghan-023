@echo off
REM QnA Bot Flask Server - Startup Script
REM This ensures the correct Python interpreter from local venv is used

cd /d "%~dp0"

echo Starting QnA Bot Flask Server...
echo.
echo Using Python: %cd%\.venv\Scripts\python.exe
echo.

REM Run Flask app with correct Python interpreter
.\.venv\Scripts\python.exe app.py

pause

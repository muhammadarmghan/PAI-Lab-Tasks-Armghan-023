@echo off
REM Setup and run Task_12 - QnA Bot

echo Creating virtual environment...
python -m venv .venv

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building FAISS index...
python pipeline_training.py

echo.
echo Starting Flask server...
python app.py

pause

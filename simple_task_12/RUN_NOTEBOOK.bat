@echo off
REM Start Jupyter Notebook for pipeline

call .venv\Scripts\activate.bat
jupyter notebook pipeline.ipynb

pause

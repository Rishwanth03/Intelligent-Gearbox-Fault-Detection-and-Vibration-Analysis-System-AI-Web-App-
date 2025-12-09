@echo off
REM Intelligent Gearbox Fault Detection System - Setup Script for Windows
REM This script sets up the development environment on Windows

echo =====================================
echo Gearbox Fault Detection System Setup
echo =====================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Generate sample data
echo Generating sample data...
python generate_sample_data.py
echo.

REM Run tests
echo Running tests...
python test_system.py
echo.

echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run: python app.py
echo   3. Open browser to: http://localhost:5000
echo.
pause

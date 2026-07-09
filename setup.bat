@echo off
REM Setup script for Windows users
REM This creates a virtual environment, installs dependencies, and runs the application

cd /d "%~dp0"

echo.
echo ========================================
echo Password Generator - First-Time Setup
echo ========================================
echo.

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Could not create virtual environment.
        echo Make sure Python is installed and added to PATH.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

echo.
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Starting Password Generator...
echo.

REM Run the application
python GEN_G2.py
if errorlevel 1 (
    echo.
    echo Error: Could not run the application.
    echo You can manually run it with: .\.venv\Scripts\activate.bat ^&^& python GEN_G2.py
    pause
    exit /b 1
)


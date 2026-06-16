@echo off
REM Setup script for Windows users
REM This creates a virtual environment and installs dependencies

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
echo You can now run the password generator with:
echo   - Double-click: run.bat
echo   - Or manually: .\.venv\Scripts\activate.bat ^&^& python GEN_G2.py
echo.

pause


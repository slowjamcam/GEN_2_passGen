@echo off
REM Quick launcher for Password Generator
REM This script activates the virtual environment and runs the password generator

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv" (
    echo.
    echo Virtual environment not found!
    echo Please run setup.bat first to set up the environment and install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run the generator
call .\.venv\Scripts\activate.bat
python GEN_G2.py

REM Check if application exited with an error
if errorlevel 1 (
    echo.
    echo Error: The application encountered an error.
    pause
    exit /b 1
)


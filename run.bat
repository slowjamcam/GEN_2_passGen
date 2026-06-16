@echo off
REM Quick launcher for Password Generator
REM This script runs the password generator without requiring PowerShell

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    pause
    exit /b 1
)

REM Activate virtual environment and run the generator
call .\.venv\Scripts\activate.bat
python GEN_G2.py

pause


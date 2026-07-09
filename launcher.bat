@echo off
REM GUI Launcher for Password Generator
REM Provides an interactive menu to launch different components of the application

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv" (
    cls
    echo.
    echo ========================================
    echo   Password Generator - Setup Required
    echo ========================================
    echo.
    echo The virtual environment has not been set up yet.
    echo.
    echo Please run "setup.bat" first to initialize the environment.
    echo.
    echo.
    pause
    exit /b 1
)

:menu
cls
echo.
echo ========================================
echo     PASSWORD GENERATOR - Main Menu
echo ========================================
echo.
echo Select an option:
echo.
echo   1. Launch CLI Password Generator (GEN_G2.py)
echo   2. Launch GUI Password Generator (gui.py)
echo   3. Search Passwords
echo   4. View Stored Passwords
echo   5. Open Project Folder
echo   6. Exit
echo.
echo ========================================
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto cli
if "%choice%"=="2" goto gui
if "%choice%"=="3" goto search
if "%choice%"=="4" goto view
if "%choice%"=="5" goto folder
if "%choice%"=="6" goto exit
if "%choice%"=="" goto menu

cls
echo.
echo Invalid choice. Please enter a number between 1 and 6.
echo.
pause
goto menu

:cli
cls
echo.
echo Starting CLI Password Generator...
echo.
call .\.venv\Scripts\activate.bat
python GEN_G2.py
if errorlevel 1 (
    echo.
    echo Error running the CLI generator.
)
pause
goto menu

:gui
cls
echo.
echo Starting GUI Password Generator...
echo.
call .\.venv\Scripts\activate.bat
start "" python gui.py
echo GUI launched in a new window.
echo.
pause
goto menu

:search
cls
echo.
echo Starting Password Search...
echo.
call .\.venv\Scripts\activate.bat
python serachpassword.py
if errorlevel 1 (
    echo.
    echo Error running the search tool.
)
pause
goto menu

:view
cls
echo.
if not exist "stored_passwords.csv" (
    echo No stored passwords file found.
    echo.
    pause
    goto menu
)
echo Stored Passwords (CSV Format):
echo ========================================
echo.
type stored_passwords.csv
echo.
echo ========================================
echo.
pause
goto menu

:folder
cls
explorer "%~dp0"
goto menu

:exit
cls
echo.
echo Thank you for using Password Generator!
echo.
exit /b 0


@echo off
title Windows Desktop AI Assistant

echo ================================================================
echo          Windows Desktop AI Assistant - Starting...
echo ================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please run INSTALL.bat first
    pause
    exit /b 1
)

:: Check if setup has been run
if not exist "config\settings.ini" (
    echo [ERROR] Setup not completed
    echo Please run INSTALL.bat first
    pause
    exit /b 1
)

echo [INFO] Starting Desktop AI Assistant...
echo [INFO] Edit 'data\commands.txt' to add commands
echo [INFO] Move mouse to screen corner for emergency stop
echo [INFO] Check 'logs\app.log' for detailed information
echo.
echo ================================================================
echo                    AI Assistant Running
echo ================================================================
echo.

:: Start the main application
python main.py

echo.
echo [INFO] AI Assistant stopped
pause
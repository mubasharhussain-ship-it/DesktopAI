@echo off
echo ================================================================
echo          Windows Desktop AI Assistant - Quick Setup
echo ================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [INFO] Python is installed
echo.

:: Run the setup script
echo [INFO] Running automated setup...
echo.
python setup.py

if errorlevel 1 (
    echo.
    echo [ERROR] Setup failed. Please check the error messages above.
    echo.
    echo Common solutions:
    echo 1. Run this as Administrator
    echo 2. Check your internet connection
    echo 3. Install Ollama from https://ollama.com/
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                    Setup Complete!
echo ================================================================
echo.
echo Next steps:
echo 1. Edit 'data\commands.txt' to add your commands
echo 2. Run 'python main.py' to start the AI assistant
echo 3. Move mouse to screen corner to emergency stop
echo.
echo For help, see README.md or COPY_TO_NEW_PC.md
echo.
pause
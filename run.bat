@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python was not found on this system.
    echo Installing Python 3.12 via winget...

    winget install Python.Python.3.12

    echo.
    echo [!] If Python is still not detected after install:
    echo     - Restart this terminal
    echo     - Or restart your PC
    echo.

    pause
    exit /b
)

echo [✓] Python detected.

echo Updating pip...
python -m pip install --upgrade pip

echo Installing required modules...
python -m pip install requests pywin32

echo.
echo Installation complete! Starting program...
echo.

python assetstealer.py

pause
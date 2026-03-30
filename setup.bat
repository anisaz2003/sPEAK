@echo off
echo === sPEAK - Installation ===
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Create venv
echo [1/3] Creating virtual environment...
python -m venv .venv

:: Install dependencies
echo [2/3] Installing dependencies...
.venv\Scripts\pip install -r requirements.txt --quiet

:: Copy config if not present
echo [3/3] Setting up config...
if not exist config.json (
    copy config.example.json config.json >nul
    echo       config.json created - edit it to customize the model and language.
) else (
    echo       config.json already exists, skipping.
)

echo.
echo === Done! ===
echo.
echo To start sPEAK:
echo   Double-click launch_wisprflow.bat
echo.
echo To launch at Windows startup:
echo   Run install_startup.bat
echo.
pause

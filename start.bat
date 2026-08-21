@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   TestPad Analyzer - launcher
echo ============================================
echo.

python --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Install Python from python.org and tick "Add Python to PATH",
    echo then run this file again.
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking dependencies: flask, pandas, openpyxl
python -c "import flask, pandas, openpyxl" >nul 2>nul
if errorlevel 1 (
    echo       Installing dependencies...
    python -m pip install --upgrade pip
    python -m pip install flask pandas openpyxl
)

echo [2/4] Checking Playwright
python -c "import playwright" >nul 2>nul
if errorlevel 1 (
    echo       Installing playwright...
    python -m pip install playwright
)

echo [3/4] Checking chromium browser
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); p.chromium.launch(headless=True).close(); p.stop()" >nul 2>nul
if errorlevel 1 (
    echo       Installing chromium...
    python -m playwright install chromium
)

echo [4/4] Checking if the server is already running
powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:5000/api/status' -TimeoutSec 2) | Out-Null; exit 0 } catch { exit 1 }" >nul 2>nul
if not errorlevel 1 (
    echo.
    echo Server is already running: http://127.0.0.1:5000
    start "" http://127.0.0.1:5000
    echo.
    pause
    exit /b 0
)

echo.
echo Starting server: http://127.0.0.1:5000
echo Do not close this window while the app is running.
echo.
start "" cmd /c "timeout /t 6 /nobreak >nul & start http://127.0.0.1:5000"
python server.py

echo.
echo Server stopped.
pause
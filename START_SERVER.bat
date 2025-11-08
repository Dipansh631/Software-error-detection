@echo off
REM Simple server startup script
echo ============================================================
echo Software Defect Detection - Server Startup
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Downloading and installing pip...
python -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')" 2>nul
if exist get-pip.py (
    echo Installing pip...
    python get-pip.py 2>nul
    del get-pip.py 2>nul
)

echo.
echo Step 2: Installing Flask and dependencies...
python -m pip install flask pandas scikit-learn numpy 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Installation may have failed. Trying to continue...
)

echo.
echo Step 3: Checking Flask...
python -c "import flask; print('Flask OK')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Flask is not installed!
    echo.
    echo Please install manually:
    echo   1. Open a new Command Prompt (not PowerShell)
    echo   2. Navigate to this folder
    echo   3. Run: python -m pip install flask pandas scikit-learn numpy
    echo   4. Then run: python app.py
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Starting Flask Server...
echo ============================================================
echo.
echo Server URL: http://127.0.0.1:5000
echo Press Ctrl+C to stop
echo.
echo ============================================================
echo.

python app.py

pause


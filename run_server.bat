@echo off
echo ============================================================
echo Starting Software Defect Detection Server
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Try to install Flask if not available
echo Checking for Flask...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Flask not found. Installing dependencies...
    python -m ensurepip --upgrade >nul 2>&1
    python -m pip install flask pandas scikit-learn numpy >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Could not install dependencies automatically.
        echo Please install manually:
        echo   python -m pip install flask pandas scikit-learn numpy
        echo.
        pause
        exit /b 1
    )
    echo Dependencies installed!
) else (
    echo Flask is installed.
)

echo.
echo ============================================================
echo Starting Flask Server...
echo ============================================================
echo.
echo Server will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python app.py

pause


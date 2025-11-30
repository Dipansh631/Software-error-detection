@echo off
echo ============================================================
echo Starting Streamlit App
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo Streamlit not found. Installing...
    pip install streamlit
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Could not install Streamlit.
        echo Please install manually: pip install streamlit
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo Starting Streamlit Server...
echo ============================================================
echo.
echo App will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

streamlit run streamlit_app.py

pause


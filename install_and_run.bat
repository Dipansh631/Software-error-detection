@echo off
echo ============================================================
echo Software Defect Detection - Installation and Run Script
echo ============================================================
echo.

REM Try to bootstrap pip if not available
python -m ensurepip --upgrade 2>nul

REM Try to install dependencies
echo [Step 1] Installing dependencies...
python -m pip install --upgrade pip 2>nul
python -m pip install pandas scikit-learn flask numpy 2>nul

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Could not install packages using pip.
    echo Please install manually:
    echo   python -m pip install pandas scikit-learn flask numpy
    echo.
    echo Or if pip is not available, try:
    echo   python -m ensurepip --upgrade
    echo   python -m pip install pandas scikit-learn flask numpy
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully!
echo.

REM Train model if needed
echo [Step 2] Checking model...
if not exist "model\defect_model.pkl" (
    echo Training model...
    python train_model.py
    if %errorlevel% neq 0 (
        echo [WARNING] Model training failed, but app will use fallback model
    ) else (
        echo [OK] Model trained successfully
    )
) else (
    echo [OK] Model already exists
)
echo.

REM Run Flask app
echo [Step 3] Starting Flask application...
echo.
echo ============================================================
echo The app will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py

pause


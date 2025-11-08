@echo off
echo ============================================================
echo Installing Dependencies from requirements.txt
echo ============================================================
echo.

REM Try multiple methods to install pip and packages

echo Method 1: Trying python -m pip...
python -m pip install -r requirements.txt 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Packages installed using python -m pip
    goto :end
)

echo Method 2: Trying py launcher...
py -m pip install -r requirements.txt 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Packages installed using py launcher
    goto :end
)

echo Method 3: Installing pip first...
python -m ensurepip --upgrade
python -m pip install -r requirements.txt 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Packages installed after ensuring pip
    goto :end
)

echo Method 4: Downloading get-pip.py...
python -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')" 2>nul
python get-pip.py 2>nul
python -m pip install -r requirements.txt 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Packages installed using get-pip.py
    goto :end
)

echo.
echo [ERROR] Could not install packages automatically.
echo.
echo Please try one of these methods manually:
echo   1. python -m pip install -r requirements.txt
echo   2. pip install -r requirements.txt
echo   3. Use a virtual environment (recommended)
echo   4. See INSTALL_DEPENDENCIES.md for detailed instructions
echo.

:end
pause


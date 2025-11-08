# Simple Server Start Guide

## The Problem
Your Python environment has pip issues, so Flask can't be installed automatically.

## Solution: Run in Command Prompt (Not PowerShell)

### Method 1: Use START_SERVER.bat

1. **Open Command Prompt** (cmd.exe, NOT PowerShell)
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to your project folder:**
   ```cmd
   cd "D:\dowl\software detection ml\Software-error-detection-main\software_defect_detection"
   ```

3. **Run the batch file:**
   ```cmd
   START_SERVER.bat
   ```

### Method 2: Manual Installation (If Method 1 Fails)

1. **Open Command Prompt** (cmd.exe)

2. **Navigate to project:**
   ```cmd
   cd "D:\dowl\software detection ml\Software-error-detection-main\software_defect_detection"
   ```

3. **Download and install pip:**
   ```cmd
   python -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')"
   python get-pip.py
   ```

4. **Install Flask:**
   ```cmd
   python -m pip install flask pandas scikit-learn numpy
   ```

5. **Start server:**
   ```cmd
   python app.py
   ```

6. **Open browser:** http://127.0.0.1:5000

### Method 3: Use Python Script

In Command Prompt:
```cmd
cd "D:\dowl\software detection ml\Software-error-detection-main\software_defect_detection"
python fix_and_run.py
```

## Why Command Prompt Instead of PowerShell?

PowerShell has different syntax and may have issues with:
- Redirection (`2>nul`)
- Error handling
- Some Python subprocess calls

Command Prompt (cmd.exe) is more compatible with batch files.

## Verify It's Working

After starting, you should see:
```
============================================================
Starting Flask Server...
============================================================

Server running at: http://127.0.0.1:5000
Press Ctrl+C to stop the server

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Then open your browser to: **http://127.0.0.1:5000**

## If Still Not Working

1. **Check Python version:**
   ```cmd
   python --version
   ```
   Should be 3.7+

2. **Try virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install flask pandas scikit-learn numpy
   python app.py
   ```

3. **Reinstall Python:**
   - Download from python.org
   - Check "Add Python to PATH"
   - Check "Install pip"


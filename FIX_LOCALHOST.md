# Fix: Localhost Not Working

## The Problem

The Flask server cannot start because **Flask is not installed**. Your Python environment also has issues with pip installation.

## Quick Fix (Choose One Method)

### Method 1: Use run_server.bat (Easiest)

Double-click or run:
```bash
run_server.bat
```

This will:
1. Check if Flask is installed
2. Install it if missing
3. Start the server automatically

### Method 2: Manual Installation

**Step 1: Install Flask**
```bash
python -m pip install flask
```

If that doesn't work, try:
```bash
python -m ensurepip --upgrade
python -m pip install flask pandas scikit-learn numpy
```

**Step 2: Start Server**
```bash
python app.py
```

**Step 3: Open Browser**
Go to: `http://127.0.0.1:5000`

### Method 3: Use Python Script

Run:
```bash
python start_server.py
```

This script will:
- Check for dependencies
- Install missing packages
- Start the server

### Method 4: Virtual Environment (Recommended)

If pip keeps failing, use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install packages
pip install flask pandas scikit-learn numpy

# Start server
python app.py
```

## Verify Installation

Check if Flask is installed:
```bash
python -c "import flask; print('Flask version:', flask.__version__)"
```

If you see a version number, Flask is installed!

## Expected Server Output

When the server starts successfully, you should see:

```
============================================================
Starting Flask Server...
============================================================

Server running at: http://127.0.0.1:5000
Press Ctrl+C to stop the server

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

## If Still Not Working

1. **Check Python installation:**
   ```bash
   python --version
   ```
   Should show Python 3.7+

2. **Reinstall Python with pip:**
   - Download Python from python.org
   - Make sure to check "Add Python to PATH"
   - Check "Install pip" during installation

3. **Use conda (if available):**
   ```bash
   conda install flask pandas scikit-learn numpy
   python app.py
   ```

4. **Check port 5000:**
   ```bash
   netstat -ano | findstr :5000
   ```
   If something is using it, kill that process or change the port in `app.py`

## Files Created to Help

- `run_server.bat` - Windows batch file to start server
- `start_server.py` - Python script to install and start
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide

## Next Steps

1. Try `run_server.bat` first (easiest)
2. If that fails, try Method 4 (virtual environment)
3. Check `TROUBLESHOOTING.md` for more details


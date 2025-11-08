# Troubleshooting: Localhost Not Working

## Problem: Server Not Starting

### Solution 1: Install Dependencies First

The most common issue is missing Flask. Run this command:

```bash
python -m pip install flask pandas scikit-learn numpy
```

If pip is not available:
```bash
python -m ensurepip --upgrade
python -m pip install flask pandas scikit-learn numpy
```

### Solution 2: Use the Startup Script

**Windows (Batch file):**
```bash
run_server.bat
```

**Python script:**
```bash
python start_server.py
```

### Solution 3: Manual Start

1. **Install dependencies:**
   ```bash
   python -m pip install flask pandas scikit-learn numpy
   ```

2. **Start the server:**
   ```bash
   python app.py
   ```

3. **Open browser:**
   Navigate to: `http://127.0.0.1:5000`

## Common Errors

### Error: "No module named 'flask'"
**Solution:** Install Flask:
```bash
python -m pip install flask
```

### Error: "No module named 'pandas'"
**Solution:** Install pandas:
```bash
python -m pip install pandas
```

### Error: "Port 5000 already in use"
**Solution:** 
1. Find and close the process using port 5000:
   ```bash
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   ```
2. Or change the port in `app.py`:
   ```python
   app.run(host='127.0.0.1', port=5001, debug=True)  # Change to 5001
   ```

### Error: "Address already in use"
**Solution:** Another process is using the port. Close it or use a different port.

### Error: "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Install scikit-learn:
```bash
python -m pip install scikit-learn
```

## Verification Steps

1. **Check if Flask is installed:**
   ```bash
   python -c "import flask; print('Flask OK')"
   ```

2. **Check if app.py exists:**
   ```bash
   python -c "import os; print('app.py exists:', os.path.exists('app.py'))"
   ```

3. **Test the server manually:**
   ```bash
   python app.py
   ```
   You should see:
   ```
   Starting Flask Server...
   Server running at: http://127.0.0.1:5000
   ```

## Quick Fix Script

Run this to install everything and start the server:

```bash
python start_server.py
```

Or on Windows:
```bash
run_server.bat
```

## Still Not Working?

1. **Check Python version:**
   ```bash
   python --version
   ```
   Should be Python 3.7 or higher.

2. **Check if you're in the right directory:**
   ```bash
   dir app.py
   ```
   Should show `app.py` file.

3. **Try a different port:**
   Edit `app.py` and change:
   ```python
   app.run(host='127.0.0.1', port=5001, debug=True)
   ```
   Then access: `http://127.0.0.1:5001`

4. **Check firewall:**
   Make sure Windows Firewall isn't blocking Python.

5. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install flask pandas scikit-learn numpy
   python app.py
   ```

## Expected Output When Server Starts

```
============================================================
Starting Flask Server...
============================================================

Server running at: http://127.0.0.1:5000
Press Ctrl+C to stop the server

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

If you see this, the server is running successfully!


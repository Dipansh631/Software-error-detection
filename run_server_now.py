"""
Run the Flask server with proper error handling and output
"""

import sys
import os
import subprocess

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("Starting Software Defect Detection Server")
print("="*60)
print()

# Check Flask
print("Step 1: Checking Flask...")
try:
    import flask
    print(f"[OK] Flask is installed (version {flask.__version__})")
except ImportError:
    print("[MISSING] Flask is not installed")
    print("Installing Flask and dependencies...")
    
    # Try to install
    try:
        # First ensure pip
        print("Ensuring pip is available...")
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                     check=False, capture_output=True)
        
        # Install Flask
        print("Installing Flask...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "flask", "pandas", "scikit-learn", "numpy"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("[OK] Dependencies installed successfully!")
        else:
            print("[ERROR] Failed to install dependencies")
            print("Error output:", result.stderr[:500] if result.stderr else "Unknown error")
            print("\nPlease install manually:")
            print("  python -m pip install flask pandas scikit-learn numpy")
            input("\nPress Enter to exit...")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Installation failed: {e}")
        print("\nPlease install manually:")
        print("  python -m pip install flask pandas scikit-learn numpy")
        input("\nPress Enter to exit...")
        sys.exit(1)

# Check other dependencies
print("\nStep 2: Checking other dependencies...")
missing = []
for pkg in ['pandas', 'sklearn', 'numpy']:
    try:
        __import__(pkg)
        print(f"[OK] {pkg}")
    except ImportError:
        print(f"[MISSING] {pkg}")
        missing.append(pkg)

if missing:
    print(f"\nInstalling missing packages: {', '.join(missing)}...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing, 
                      check=True, timeout=300)
        print("[OK] Missing packages installed")
    except:
        print("[WARNING] Some packages may be missing, but continuing...")

# Check app.py
print("\nStep 3: Checking app.py...")
if not os.path.exists('app.py'):
    print("[ERROR] app.py not found!")
    input("\nPress Enter to exit...")
    sys.exit(1)
print("[OK] app.py found")

# Start server
print("\n" + "="*60)
print("Starting Flask Server...")
print("="*60)
print()
print("Server will be available at: http://127.0.0.1:5000")
print("Press Ctrl+C to stop the server")
print()
print("="*60)
print()

try:
    import app
    app.app.run(host='127.0.0.1', port=5000, debug=True)
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
except Exception as e:
    print(f"\n[ERROR] Failed to start server: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")


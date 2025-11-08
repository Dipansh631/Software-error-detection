"""
Fix pip and install dependencies, then run the server
"""

import sys
import os
import subprocess
import urllib.request

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("FIXING AND STARTING SERVER")
print("="*70)
print()

# Step 1: Fix pip
print("Step 1: Fixing pip installation...")
try:
    # Try ensurepip
    print("  Trying ensurepip...")
    result = subprocess.run(
        [sys.executable, "-m", "ensurepip", "--upgrade"],
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode == 0:
        print("  [OK] ensurepip completed")
    else:
        print("  [WARNING] ensurepip had issues, trying get-pip.py...")
        
        # Download get-pip.py
        try:
            print("  Downloading get-pip.py...")
            urllib.request.urlretrieve(
                'https://bootstrap.pypa.io/get-pip.py',
                'get-pip.py'
            )
            print("  [OK] Downloaded get-pip.py")
            
            # Run get-pip.py
            print("  Installing pip...")
            result = subprocess.run(
                [sys.executable, "get-pip.py"],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                print("  [OK] pip installed via get-pip.py")
            else:
                print("  [WARNING] get-pip.py had issues")
                print("  Error:", result.stderr[:200] if result.stderr else "Unknown")
        except Exception as e:
            print(f"  [WARNING] Could not use get-pip.py: {e}")
except Exception as e:
    print(f"  [WARNING] Error with ensurepip: {e}")

# Step 2: Check if pip works now
print("\nStep 2: Verifying pip...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print(f"  [OK] pip is working: {result.stdout.strip()}")
        pip_works = True
    else:
        print("  [ERROR] pip is not working")
        pip_works = False
except Exception as e:
    print(f"  [ERROR] pip check failed: {e}")
    pip_works = False

# Step 3: Install Flask and dependencies
if pip_works:
    print("\nStep 3: Installing Flask and dependencies...")
    packages = ['flask', 'pandas', 'scikit-learn', 'numpy']
    
    for package in packages:
        print(f"  Installing {package}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print(f"  [OK] {package} installed")
            else:
                print(f"  [FAILED] {package} installation failed")
                if result.stderr:
                    print(f"    Error: {result.stderr[:200]}")
        except Exception as e:
            print(f"  [ERROR] Exception installing {package}: {e}")
else:
    print("\nStep 3: SKIPPED - pip is not working")
    print("\n[CRITICAL] Cannot install packages without pip.")
    print("\nPlease fix pip manually:")
    print("  1. Download get-pip.py from: https://bootstrap.pypa.io/get-pip.py")
    print("  2. Run: python get-pip.py")
    print("  3. Then run this script again")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Step 4: Verify Flask is installed
print("\nStep 4: Verifying Flask installation...")
try:
    import flask
    print(f"  [OK] Flask is installed (version {flask.__version__})")
except ImportError:
    print("  [ERROR] Flask is still not installed!")
    print("\n[CRITICAL] Flask installation failed.")
    print("Please install manually:")
    print("  python -m pip install flask")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Step 5: Check other dependencies
print("\nStep 5: Checking other dependencies...")
missing = []
for pkg in [('pandas', 'pandas'), ('sklearn', 'scikit-learn'), ('numpy', 'numpy')]:
    try:
        __import__(pkg[0])
        print(f"  [OK] {pkg[1]}")
    except ImportError:
        print(f"  [MISSING] {pkg[1]}")
        missing.append(pkg[1])

if missing:
    print(f"\n  Installing missing: {', '.join(missing)}...")
    for pkg in missing:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg], 
                      capture_output=True, timeout=300)

# Step 6: Start the server
print("\n" + "="*70)
print("STARTING FLASK SERVER")
print("="*70)
print()
print("Server will be available at: http://127.0.0.1:5000")
print("Press Ctrl+C to stop the server")
print()
print("="*70)
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


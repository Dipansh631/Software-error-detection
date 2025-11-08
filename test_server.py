"""
Simple test script to check if server can start
"""

import sys
import os

print("="*60)
print("Server Startup Test")
print("="*60)
print()

# Check Flask
print("1. Checking Flask...")
try:
    import flask
    print("   [OK] Flask is installed")
    print(f"   Version: {flask.__version__}")
except ImportError:
    print("   [MISSING] Flask is not installed")
    print("   Run: python -m pip install flask")
    sys.exit(1)

# Check other dependencies
print("\n2. Checking other dependencies...")
deps = {
    'pandas': 'pandas',
    'sklearn': 'scikit-learn',
    'numpy': 'numpy'
}

missing = []
for module, package in deps.items():
    try:
        __import__(module)
        print(f"   [OK] {package}")
    except ImportError:
        print(f"   [MISSING] {package}")
        missing.append(package)

if missing:
    print(f"\n   Install missing: python -m pip install {' '.join(missing)}")

# Check app.py
print("\n3. Checking app.py...")
if os.path.exists('app.py'):
    print("   [OK] app.py exists")
else:
    print("   [ERROR] app.py not found!")
    print("   Make sure you're in the correct directory")
    sys.exit(1)

# Check utils
print("\n4. Checking utility modules...")
utils_ok = True
for util in ['utils.static_analysis', 'utils.feature_extract']:
    try:
        __import__(util)
        print(f"   [OK] {util}")
    except ImportError as e:
        print(f"   [ERROR] {util}: {e}")
        utils_ok = False

if not utils_ok:
    print("\n   [WARNING] Some utility modules missing, but server may still work")

# Final check
print("\n" + "="*60)
if not missing and utils_ok:
    print("[SUCCESS] All checks passed! Server should start.")
    print("\nTo start the server, run:")
    print("  python app.py")
    print("\nOr use:")
    print("  run_server.bat")
else:
    print("[WARNING] Some issues found. Fix them before starting server.")
print("="*60)


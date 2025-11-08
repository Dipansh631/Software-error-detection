"""
Script to install dependencies and start the Flask server
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        print(f"Installing {package}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"[OK] {package} installed successfully")
            return True
        else:
            print(f"[FAILED] Could not install {package}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Installation of {package} took too long")
        return False
    except Exception as e:
        print(f"[ERROR] Error installing {package}: {e}")
        return False

def check_and_install_dependencies():
    """Check and install required packages."""
    required_packages = ['flask', 'pandas', 'scikit-learn', 'numpy']
    
    print("="*60)
    print("Checking Dependencies")
    print("="*60)
    print()
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"[OK] {package} is installed")
        except ImportError:
            print(f"[MISSING] {package} is not installed")
            missing_packages.append(package)
    
    if not missing_packages:
        print("\nAll required packages are installed!")
        return True
    
    print(f"\nInstalling {len(missing_packages)} missing packages...")
    print("This may take a few minutes...\n")
    
    # First ensure pip is available
    try:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                      check=True, capture_output=True)
    except:
        pass
    
    success_count = 0
    for package in missing_packages:
        if install_package(package):
            success_count += 1
        print()
    
    if success_count == len(missing_packages):
        print("All packages installed successfully!")
        return True
    else:
        print(f"Warning: Only {success_count}/{len(missing_packages)} packages installed")
        print("The server may not work properly if critical packages are missing.")
        return success_count > 0

def start_flask_server():
    """Start the Flask server."""
    print("\n" + "="*60)
    print("Starting Flask Server")
    print("="*60)
    print()
    
    try:
        import app
        print("Server starting at: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server\n")
        app.app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except ImportError as e:
        print(f"[ERROR] Could not import app: {e}")
        print("Make sure you're in the correct directory and app.py exists.")
        return False
    except Exception as e:
        print(f"[ERROR] Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function."""
    print("\n" + "="*60)
    print("Software Defect Detection - Server Startup")
    print("="*60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("\n[ERROR] Failed to install required dependencies.")
        print("Please install manually:")
        print("  python -m pip install flask pandas scikit-learn numpy")
        return
    
    # Start server
    start_flask_server()

if __name__ == "__main__":
    main()


"""
Setup and Run Script for Software Defect Detection Project

This script will:
1. Check and install required dependencies
2. Train the model if needed
3. Run the Flask app on localhost
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        print(f"Warning: Could not install {package}")
        return False
    except Exception as e:
        print(f"Error installing {package}: {e}")
        return False

def check_and_install_dependencies():
    """Check if required packages are installed and install if missing."""
    required_packages = {
        'pandas': 'pandas',
        'sklearn': 'scikit-learn',
        'flask': 'flask',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"[OK] {package_name} is installed")
        except ImportError:
            print(f"[MISSING] {package_name} is missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        print("This may take a few minutes...\n")
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"[OK] {package} installed successfully\n")
            else:
                print(f"[FAILED] Failed to install {package}\n")
                return False
    else:
        print("\nAll required packages are installed!")
    
    return True

def train_model_if_needed():
    """Train the model if it doesn't exist."""
    model_path = os.path.join('model', 'defect_model.pkl')
    
    if os.path.exists(model_path):
        print(f"\n[OK] Model already exists at {model_path}")
        return True
    
    print("\nModel not found. Training model...")
    try:
        import train_model
        train_model.main()
        print("[OK] Model trained successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Error training model: {e}")
        print("The app will use a fallback model if available.")
        return False

def run_flask_app():
    """Run the Flask application."""
    print("\n" + "="*60)
    print("Starting Flask application on localhost...")
    print("="*60)
    print("\nThe app will be available at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        import app
        app.app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] Error running Flask app: {e}")
        return False
    
    return True

def main():
    """Main execution function."""
    print("="*60)
    print("Software Defect Detection - Setup and Run")
    print("="*60)
    
    # Step 1: Check and install dependencies
    print("\n[Step 1] Checking dependencies...")
    if not check_and_install_dependencies():
        print("\n[ERROR] Failed to install all dependencies.")
        print("Please install them manually using:")
        print("  python -m pip install pandas scikit-learn flask numpy")
        print("\nOr if pip is not available, you may need to:")
        print("  1. Reinstall Python with pip included")
        print("  2. Or use a package manager like conda")
        return
    
    # Step 2: Train model if needed
    print("\n[Step 2] Checking model...")
    train_model_if_needed()
    
    # Step 3: Run Flask app
    print("\n[Step 3] Starting Flask application...")
    run_flask_app()

if __name__ == "__main__":
    main()


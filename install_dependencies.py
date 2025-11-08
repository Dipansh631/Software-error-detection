"""
Script to install all dependencies from requirements.txt
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a single package."""
    try:
        print(f"Installing {package}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[OK] Successfully installed {package}")
            return True
        else:
            print(f"[FAILED] Failed to install {package}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error installing {package}: {e}")
        return False

def main():
    """Install all dependencies from requirements.txt"""
    print("="*60)
    print("Installing Dependencies from requirements.txt")
    print("="*60)
    print()
    
    # First, ensure pip is available
    print("Step 1: Ensuring pip is available...")
    try:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
        print("[OK] Pip is available")
    except Exception as e:
        print(f"[ERROR] Could not ensure pip: {e}")
        return
    
    print()
    
    # Read requirements.txt
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found!")
        return
    
    print(f"Step 2: Reading {requirements_file}...")
    with open(requirements_file, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    
    print(f"Found {len(packages)} packages to install:")
    for pkg in packages:
        print(f"  - {pkg}")
    print()
    
    # Try installing all at once first
    print("Step 3: Attempting to install all packages at once...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("[OK] All packages installed successfully!")
            print(result.stdout)
            return
        else:
            print("[FAILED] Batch installation failed, trying individual packages...")
            print(result.stderr)
    except Exception as e:
        print(f"[ERROR] Batch installation error: {e}")
        print("Trying individual packages...")
    
    print()
    
    # Install packages one by one
    print("Step 4: Installing packages individually...")
    success_count = 0
    failed_packages = []
    
    for package in packages:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
        print()
    
    # Summary
    print("="*60)
    print("Installation Summary")
    print("="*60)
    print(f"Successfully installed: {success_count}/{len(packages)}")
    if failed_packages:
        print(f"Failed packages: {', '.join(failed_packages)}")
        print("\nYou may need to install these manually or check for errors above.")
    else:
        print("[OK] All packages installed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()


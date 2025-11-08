# Quick Start Guide - Software Defect Detection

## ✅ Fixed Issues in train_model.py

1. **Fixed dataset path**: Now correctly looks for PROMISE datasets in the `datasets/` folder
2. **Fixed app.py model path**: Now uses correct relative path to model file

## 🚀 Running the Project

### Method 1: Use the Batch Script (Recommended for Windows)
```bash
install_and_run.bat
```

### Method 2: Manual Steps

#### Step 1: Install Pip (if not available)
```bash
python -m ensurepip --upgrade
```

#### Step 2: Install Dependencies
```bash
python -m pip install pandas scikit-learn flask numpy
```

#### Step 3: Train the Model
```bash
python train_model.py
```

#### Step 4: Run the Flask App
```bash
python app.py
```

#### Step 5: Open in Browser
Navigate to: **http://127.0.0.1:5000**

## 📋 What Was Fixed

### train_model.py
- ✅ Fixed path to look for datasets in `datasets/` folder instead of workspace root
- ✅ Added better error messages

### app.py  
- ✅ Fixed hardcoded path to use relative paths
- ✅ Now correctly finds the model file

## 🎯 Features

The web application provides:
- Upload source code files
- Static analysis metrics display
- Defect prediction (Defective/Clean)
- Clean, modern UI

## 📝 Notes

- If dependencies can't be installed, you may need to:
  1. Use a virtual environment: `python -m venv venv` then `venv\Scripts\activate`
  2. Or use conda: `conda install pandas scikit-learn flask numpy`
  3. Or reinstall Python with pip included

- The app will work with a fallback model if training fails
- All datasets should be in the `datasets/` folder


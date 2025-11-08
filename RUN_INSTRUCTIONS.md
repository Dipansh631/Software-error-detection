# How to Run the Software Defect Detection Project

## Quick Start

### Option 1: Using the Batch Script (Windows)
```bash
install_and_run.bat
```

### Option 2: Using the Python Setup Script
```bash
python setup_and_run.py
```

### Option 3: Manual Setup

#### Step 1: Install Dependencies
If pip is available:
```bash
python -m pip install pandas scikit-learn flask numpy
```

If pip is not available, first install it:
```bash
python -m ensurepip --upgrade
python -m pip install pandas scikit-learn flask numpy
```

#### Step 2: Train the Model
```bash
python train_model.py
```

#### Step 3: Run the Flask App
```bash
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

## Troubleshooting

### Issue: "No module named pip"
**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue: "ModuleNotFoundError" for pandas, sklearn, flask, etc.
**Solution:**
Make sure all dependencies are installed:
```bash
python -m pip install pandas scikit-learn flask numpy
```

### Issue: Model not found
**Solution:**
The app will use a fallback model automatically, but for best results, train the model first:
```bash
python train_model.py
```

### Issue: Port 5000 already in use
**Solution:**
Edit `app.py` and change the port number:
```python
app.run(host='127.0.0.1', port=5001, debug=True)  # Change 5000 to 5001
```

## Project Structure

- `app.py` - Flask web application
- `train_model.py` - Model training script
- `ml_defect_detection.py` - Complete ML pipeline with 8 models
- `setup_and_run.py` - Automated setup and run script
- `install_and_run.bat` - Windows batch script for setup
- `datasets/` - Contains training datasets
- `model/` - Contains trained models (created after training)
- `utils/` - Utility modules for feature extraction and analysis

## Features

The web application allows you to:
1. Upload source code files (.py, .java, .js, .cpp, etc.)
2. View static analysis metrics
3. Get defect predictions (Defective or Clean)

## Notes

- The app uses a trained RandomForest model by default
- If no model is found, it uses a fallback synthetic model
- Static analysis metrics are heuristic and for demonstration purposes


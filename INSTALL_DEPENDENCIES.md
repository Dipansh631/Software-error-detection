# Installing Dependencies

Due to some Python environment configuration issues, here are multiple ways to install the dependencies:

## Method 1: Using pip directly (if available)

```bash
pip install -r requirements.txt
```

## Method 2: Using Python's pip module

```bash
python -m pip install -r requirements.txt
```

## Method 3: Install packages individually

If batch installation fails, install each package one by one:

```bash
python -m pip install pandas>=1.5.0
python -m pip install numpy>=1.23.0
python -m pip install scikit-learn>=1.2.0
python -m pip install matplotlib>=3.6.0
python -m pip install seaborn>=0.12.0
python -m pip install joblib>=1.2.0
python -m pip install xgboost>=1.7.0
```

## Method 4: Using get-pip.py

1. Download get-pip.py:
   ```bash
   python -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')"
   ```

2. Install pip:
   ```bash
   python get-pip.py
   ```

3. Then install requirements:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Method 5: Using a Virtual Environment (Recommended)

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate it:
   - Windows PowerShell: `venv\Scripts\Activate.ps1`
   - Windows CMD: `venv\Scripts\activate.bat`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Method 6: Using Conda (if available)

```bash
conda install pandas numpy scikit-learn matplotlib seaborn joblib
conda install -c conda-forge xgboost
```

## Troubleshooting

If you encounter "No module named pip":
1. Try: `python -m ensurepip --upgrade`
2. Or download and run get-pip.py manually
3. Or reinstall Python with pip included

## Required Packages

- pandas>=1.5.0
- numpy>=1.23.0
- scikit-learn>=1.2.0
- matplotlib>=3.6.0
- seaborn>=0.12.0
- joblib>=1.2.0
- xgboost>=1.7.0

## Verify Installation

After installation, verify by running:
```bash
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, joblib; print('All packages installed successfully!')"
```


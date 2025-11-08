# 🔍 Software Defect Detection System

A minimal, Python-only demo that combines simple static analysis metrics with a scikit-learn model to classify uploaded source code as Defective or Clean.

## What this project does
- Computes basic static analysis metrics (LOC, comments, functions, a rough complexity proxy, average line length, TODOs).
- Extracts features and predicts with a trained RandomForest model.
- Provides a simple Flask UI to upload a file and view metrics plus prediction.

## Project structure
```
software_defect_detection/
 ├── app.py                 # Flask web app
 ├── train_model.py         # Train and save the model
 ├── model/
 │    └── defect_model.pkl  # Saved ML model (created after training)
 ├── utils/
 │    ├── static_analysis.py
 │    └── feature_extract.py
 ├── datasets/
 │    └── sample.csv        # Sample dataset for training
 └── README.md
```

## Requirements
- Python 3.9+
- pandas, numpy, scikit-learn, Flask

### Install
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -U pip
pip install flask scikit-learn pandas numpy
```

## Train the model
By default, the training script will look for PROMISE datasets in your workspace root (same folder where your `.arff`/`.csv` like `cm1.csv`, `kc1.csv`, `kc2.csv`, `pc1.csv`, `jm1.csv` are located). If found, it automatically uses them; otherwise it falls back to the small sample dataset.
```bash
python software_defect_detection/train_model.py
```
This creates `software_defect_detection/model/defect_model.pkl`.

### Accuracy (demo)
On the provided sample dataset, a RandomForest typically reaches ~0.85–1.0 accuracy depending on the random split. With PROMISE datasets (CM1/KC1/KC2/PC1/JM1), accuracy depends on the combined distribution; your run prints exact metrics and a classification report.

## Run the web app
```bash
python software_defect_detection/app.py
```
Open `http://127.0.0.1:5000` in your browser. Upload a code file and click "Analyze Code" to see metrics and the prediction.

## Notes
- Metrics are heuristic and simplified for demonstration; they are not a replacement for full static analysis.
- If the trained model file is missing, the app will use a small synthetic fallback model so you can still test the UI.
- The UI is intentionally minimal and uses no external JS frameworks.

## License
MIT



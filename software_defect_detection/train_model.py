"""Train an ML model for software defect detection using a sample dataset.

This script reads `datasets/sample.csv`, trains a RandomForest classifier on
static-analysis-like features, evaluates accuracy with a hold-out split, and
saves the trained model to `model/defect_model.pkl`.
"""

import os
import pickle
from typing import Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from utils.feature_extract import FEATURE_COLUMNS
from utils.promise_ingest import load_promise_datasets


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Load the dataset containing features and labels.

    The dataset must include FEATURE_COLUMNS and a `label` column (0/1).
    """
    df = pd.read_csv(csv_path)
    missing = [c for c in FEATURE_COLUMNS + ["label"] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")
    return df


def train_model(df: pd.DataFrame) -> Tuple[RandomForestClassifier, float, str]:
    """Train the model and return (model, accuracy, report)."""
    X = df[FEATURE_COLUMNS]
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred)
    return model, acc, report


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "datasets", "sample.csv")
    model_dir = os.path.join(base_dir, "model")
    model_path = os.path.join(model_dir, "defect_model.pkl")

    os.makedirs(model_dir, exist_ok=True)

    # Try to load PROMISE datasets from the workspace root if available
    workspace_root = os.path.dirname(os.path.dirname(base_dir))
    promise_df = load_promise_datasets(workspace_root)
    if promise_df is not None and len(promise_df) > 0:
        df = promise_df
        print(f"Loaded PROMISE datasets: {len(df)} rows")
    else:
        df = load_dataset(data_path)
    model, acc, report = train_model(df)

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("Model saved to:", model_path)
    print("Accuracy:", round(acc, 4))
    print("Classification report:\n", report)


if __name__ == "__main__":
    main()



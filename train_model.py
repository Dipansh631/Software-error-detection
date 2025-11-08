"""Train an ML model for software defect detection using a sample dataset.

This script reads `datasets/sample.csv`, trains a RandomForest classifier on
static-analysis-like features, evaluates accuracy with a hold-out split, and
saves the trained model to `model/defect_model.pkl`.
"""

import os
import sys
import pickle
from typing import Tuple

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from utils.feature_extract import FEATURE_COLUMNS
from utils.promise_ingest import load_promise_datasets


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Load the dataset containing features and labels.

    The dataset must include FEATURE_COLUMNS and a `label` column (0/1).
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        DataFrame with features and labels
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If required columns are missing
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file {csv_path}: {str(e)}")
    
    if df.empty:
        raise ValueError(f"Dataset file {csv_path} is empty")
    
    missing = [c for c in FEATURE_COLUMNS + ["label"] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")
    
    # Check for missing values in features
    missing_values = df[FEATURE_COLUMNS].isnull().sum()
    if missing_values.sum() > 0:
        print(f"Warning: Found missing values in features:\n{missing_values[missing_values > 0]}")
        # Fill missing values with median for numeric columns
        for col in FEATURE_COLUMNS:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        print("Missing values filled with median.")
    
    return df


def train_model(df: pd.DataFrame) -> Tuple[RandomForestClassifier, float, str]:
    """Train the model and return (model, accuracy, report).
    
    Args:
        df: DataFrame with features and labels
        
    Returns:
        Tuple of (trained_model, accuracy, classification_report)
        
    Raises:
        ValueError: If dataset is too small or has invalid data
    """
    if len(df) < 10:
        raise ValueError(f"Dataset too small: {len(df)} samples. Need at least 10 samples.")
    
    X = df[FEATURE_COLUMNS].copy()
    y = df["label"].astype(int)
    
    # Check for valid label values
    unique_labels = y.unique()
    if len(unique_labels) < 2:
        raise ValueError(f"Dataset has only one class: {unique_labels}. Need at least 2 classes.")
    
    # Check for NaN or infinite values
    if X.isnull().any().any():
        raise ValueError("Features contain NaN values after preprocessing")
    if np.isinf(X.values).any():
        raise ValueError("Features contain infinite values")
    
    # Use stratify only if we have enough samples per class
    value_counts = y.value_counts()
    can_stratify = len(y) >= 20 and len(value_counts) >= 2 and all(value_counts >= 2)
    stratify_param = y if can_stratify else None
    if stratify_param is None:
        print("Warning: Using non-stratified split (dataset too small or imbalanced)")
    
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=stratify_param
        )
    except ValueError as e:
        # If stratify fails, try without it
        print(f"Warning: Stratified split failed: {e}. Using non-stratified split.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=None
        )
    
    if len(X_train) < 5:
        raise ValueError(f"Training set too small: {len(X_train)} samples")
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples")
    print(f"Class distribution - Train: {y_train.value_counts().to_dict()}, Test: {y_test.value_counts().to_dict()}")
    
    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred)
    return model, acc, report


def main() -> None:
    """Main function to train and save the model."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "datasets", "sample.csv")
    model_dir = os.path.join(base_dir, "model")
    model_path = os.path.join(model_dir, "defect_model.pkl")

    try:
        os.makedirs(model_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating model directory: {e}")
        sys.exit(1)

    # Try to load PROMISE datasets from the datasets folder first
    datasets_dir = os.path.join(base_dir, "datasets")
    df = None
    
    try:
        promise_df = load_promise_datasets(datasets_dir)
        if promise_df is not None and len(promise_df) > 0:
            df = promise_df
            print(f"Loaded PROMISE datasets: {len(df)} rows")
    except Exception as e:
        print(f"Warning: Error loading PROMISE datasets: {e}")
        print("Falling back to sample dataset...")
    
    # Fallback to sample.csv if PROMISE datasets not available
    if df is None or len(df) == 0:
        if not os.path.exists(data_path):
            print(f"Error: Sample dataset not found at {data_path}")
            print("Please ensure at least one dataset is available in the datasets/ folder")
            sys.exit(1)
        
        try:
            print("Loading sample dataset...")
            df = load_dataset(data_path)
            print(f"Loaded sample dataset: {len(df)} rows")
        except Exception as e:
            print(f"Error loading sample dataset: {e}")
            sys.exit(1)
    
    # Train the model
    try:
        model, acc, report = train_model(df)
    except Exception as e:
        print(f"Error training model: {e}")
        sys.exit(1)
    
    # Save the model
    try:
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        print(f"\n{'='*60}")
        print("SUCCESS: Model trained and saved!")
        print(f"{'='*60}")
        print(f"Model saved to: {model_path}")
        print(f"Accuracy: {round(acc, 4)}")
        print(f"\nClassification report:\n{report}")
    except Exception as e:
        print(f"Error saving model: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()



import os
import pickle
from typing import Dict, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier


FEATURE_COLUMNS = [
    "loc",
    "num_comments",
    "num_functions",
    "cyclomatic_complexity_estimate",
    "avg_line_length",
    "num_todos",
]


def metrics_to_features(metrics: Dict[str, float]) -> pd.DataFrame:
    """Map computed metrics to a one-row pandas DataFrame of features.

    Ensures consistent ordering and presence of all required feature columns.
    Missing metrics default to 0.0.
    """
    row = {name: float(metrics.get(name, 0.0)) for name in FEATURE_COLUMNS}
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def _train_fallback_model() -> RandomForestClassifier:
    """Train a tiny fallback model on synthetic data (for demo/first run).

    This ensures the app works even before running the full training script.
    """
    import numpy as np
    rng = np.random.default_rng(42)
    n = 128
    X = rng.normal(loc=0.0, scale=1.0, size=(n, len(FEATURE_COLUMNS)))
    # Create a synthetic decision boundary: higher complexity and todos => more defects
    y = (X[:, FEATURE_COLUMNS.index("cyclomatic_complexity_estimate")] +
         0.8 * X[:, FEATURE_COLUMNS.index("num_todos")] +
         0.4 * X[:, FEATURE_COLUMNS.index("loc")] > 0.5).astype(int)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model


def load_or_train_model(model_path: str) -> Tuple[RandomForestClassifier, str]:
    """Load a trained model if available; otherwise train a fallback model.

    Returns the model and a human-friendly model name string.
    """
    try:
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model, f"Loaded saved model ({os.path.basename(model_path)})"
    except Exception:
        # Fall through to fallback
        pass

    model = _train_fallback_model()
    return model, "Fallback RandomForest (synthetic)"



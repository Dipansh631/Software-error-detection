import os
from typing import List, Optional

import pandas as pd

from .feature_extract import FEATURE_COLUMNS


PROMISE_FILENAMES = [
    "cm1.csv", "kc1.csv", "kc2.csv", "pc1.csv", "jm1.csv",
]


def _map_promise_to_features(df: pd.DataFrame) -> pd.DataFrame:
    """Map PROMISE dataset columns into the app's FEATURE_COLUMNS schema.

    Expected columns (some optional depending on dataset):
      - loc
      - v(g) (cyclomatic complexity)
      - lOComment (lines of comments)
      - n (Halstead total operators+operands) -> used to estimate avg line length
      - defects (boolean-like)

    Notes:
      - num_functions and num_todos are not present; set to 0.0 as placeholders.
      - avg_line_length approximated by n / max(loc, 1).
    """
    df_local = df.copy()

    # Normalize label
    if "defects" in df_local.columns:
        df_local["label"] = df_local["defects"].astype(str).str.lower().map({"true": 1, "false": 0})
    elif "label" in df_local.columns:
        df_local["label"] = df_local["label"].astype(int)
    else:
        raise ValueError("PROMISE dataset missing 'defects' or 'label' column")

    # Extract source columns with fallbacks
    loc = df_local.get("loc")
    if loc is None:
        # fall back to other line counts if needed
        loc = df_local.get("lOCode")
        if loc is None:
            loc = df_local.get("locCodeAndComment")
    if loc is None:
        raise ValueError("PROMISE dataset missing a loc column (e.g., 'loc')")

    v_g = df_local.get("v(g)")
    if v_g is None:
        v_g = df_local.get("branchCount")  # weaker proxy
    if v_g is None:
        raise ValueError("PROMISE dataset missing complexity column 'v(g)' or 'branchCount'")

    lOComment = df_local.get("lOComment", pd.Series([0.0] * len(df_local)))
    n_total = df_local.get("n", pd.Series([0.0] * len(df_local)))

    # Compute engineered features
    avg_line_length = (n_total.astype(float) / loc.replace(0, 1).astype(float)).astype(float)

    features = pd.DataFrame({
        "loc": loc.astype(float),
        "num_comments": lOComment.astype(float),
        "num_functions": 0.0,  # placeholder, not in PROMISE
        "cyclomatic_complexity_estimate": v_g.astype(float),
        "avg_line_length": avg_line_length.astype(float),
        "num_todos": 0.0,  # placeholder, not in PROMISE
        "label": df_local["label"].astype(int),
    })

    # Ensure column order
    return features[[*FEATURE_COLUMNS, "label"]]


def load_promise_datasets(base_dir: str) -> Optional[pd.DataFrame]:
    """Load and combine available PROMISE CSVs from base_dir.

    Returns None if no known files exist.
    """
    dataframes: List[pd.DataFrame] = []
    for name in PROMISE_FILENAMES:
        path = os.path.join(base_dir, name)
        if not os.path.exists(path):
            continue
        try:
            df_raw = pd.read_csv(path)
            df_mapped = _map_promise_to_features(df_raw)
            dataframes.append(df_mapped)
        except Exception:
            # Skip problematic files but continue loading others
            continue

    if not dataframes:
        return None
    combined = pd.concat(dataframes, axis=0, ignore_index=True)
    combined = combined.dropna().reset_index(drop=True)
    return combined



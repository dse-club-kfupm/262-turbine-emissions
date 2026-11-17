"""Submission entry point for 262-turbine-emissions.

The committee calls predict(df) once on the hidden test set. df has the test
columns described in the README. Return a number (NOx in mg/m³) per row,
in the same order as the rows of df.

predict.py may load a model saved in models/ or train one from data/train.csv
when it runs. Use only pandas, NumPy and scikit-learn.
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = REPO_ROOT / "data" / "train.csv"


def predict(df: pd.DataFrame) -> list:
    # Baseline: the training average of NOX.
    # Replace this with your model.
    train = pd.read_csv(TRAIN_PATH)
    return [float(train["NOX"].mean())] * len(df)

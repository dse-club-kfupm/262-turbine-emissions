"""Submission entry point for 262-world-cup-oracle.

The committee calls predict(df) once on the hidden test set. df has the test
columns described in the README. Return one of "home_win", "draw" or "away_win" per row,
in the same order as the rows of df.

predict.py may load a model saved in models/ or train one from data/train.csv
when it runs. Use only pandas, NumPy and scikit-learn.
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = REPO_ROOT / "data" / "train.csv"


def predict(df: pd.DataFrame) -> list:
    # Baseline: always predict a win for the first-listed team.
    # Replace this with your model.
    return ["home_win"] * len(df)

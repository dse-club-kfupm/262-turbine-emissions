"""Check that src/predict.py loads and returns predictions in the required format.

Run from the repository root:  python tests/check_submission.py
This does not score the model; it only checks the format.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DROP = ['home_score', 'away_score', 'result']
ALLOWED = ['home_win', 'draw', 'away_win']


def main() -> int:
    sample = pd.read_csv(ROOT / "data" / "train.csv")
    sample = sample.sample(n=min(200, len(sample)), random_state=0).reset_index(drop=True)
    features = sample.drop(columns=DROP)

    from src.predict import predict

    predictions = list(predict(features))
    if len(predictions) != len(features):
        print(f"Failed: {len(predictions)} predictions for {len(features)} rows.")
        return 1
    if ALLOWED is None:
        values = pd.to_numeric(pd.Series(predictions), errors="coerce")
        if values.isna().any():
            print("Failed: every prediction must be a number.")
            return 1
    else:
        invalid = sorted({str(v) for v in predictions if v not in ALLOWED})
        if invalid:
            print(f"Failed: invalid values {invalid}. Allowed values: {ALLOWED}.")
            return 1
    print(f"Format check passed: {len(predictions)} valid predictions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

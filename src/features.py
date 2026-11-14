"""Cleaning and feature functions shared by the notebooks and src/predict.py."""

import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of df.

    Add the cleaning steps you decide on in notebook 01. The same function must
    work on the training data and on the hidden test data, which has every
    column except the target.
    """
    return df.copy()

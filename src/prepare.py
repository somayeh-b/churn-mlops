"""
prepare.py — DVC Stage 1: PREPARE
Cleans the raw churn CSV, encodes categorical features, splits into
train/test sets, and writes processed artifacts consumed by train.py.

The transformation logic lives in clean_and_split() so it can be unit
tested directly (see tests/test_pipeline.py) without touching the
filesystem or params.yaml.
"""
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

TARGET = "Churn"


def clean_and_split(df: pd.DataFrame, test_size: float, random_state: int):
    """Pure transformation: raw churn dataframe -> (train_df, test_df, encoders).

    No file I/O here on purpose, so this function is directly unit-testable.
    """
    df = df.copy()
    df = df.drop(columns=["customerID"])
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

    df[TARGET] = (df[TARGET] == "Yes").astype(int)

    cat_cols = df.select_dtypes(include="object").columns.tolist()
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    train_df = X_train.copy()
    train_df[TARGET] = y_train
    test_df = X_test.copy()
    test_df[TARGET] = y_test
    return train_df, test_df, encoders


def main():
    with open("params.yaml") as f:
        params = yaml.safe_load(f)["prepare"]

    df = pd.read_csv("data/raw/churn.csv")
    train_df, test_df, encoders = clean_and_split(
        df, test_size=params["test_size"], random_state=params["random_state"]
    )

    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    joblib.dump(encoders, "models/label_encoders.pkl")

    train_df.to_csv("data/processed/train.csv", index=False)
    test_df.to_csv("data/processed/test.csv", index=False)

    print(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
    print(f"Train churn rate: {train_df[TARGET].mean():.2%}, Test churn rate: {test_df[TARGET].mean():.2%}")


if __name__ == "__main__":
    main()

"""
Unit tests for the pipeline logic in prepare.py and train.py.

Unlike tests/test_api.py (which exercises the FastAPI layer), these tests
target the pure, file-I/O-free functions extracted specifically so they can
be tested without touching data/raw/churn.csv, params.yaml, or MLflow:
  - prepare.clean_and_split()
  - train.build_model()
  - train.compute_metrics()
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from prepare import clean_and_split
from train import build_model, compute_metrics


def _make_fake_raw_df(n=40):
    """A tiny, valid-looking raw churn dataframe for pipeline unit tests."""
    rng = np.random.RandomState(0)
    return pd.DataFrame({
        "customerID": [f"id-{i}" for i in range(n)],
        "gender": rng.choice(["Male", "Female"], n),
        "SeniorCitizen": rng.choice([0, 1], n),
        "Partner": rng.choice(["Yes", "No"], n),
        "Dependents": rng.choice(["Yes", "No"], n),
        "tenure": rng.randint(0, 72, n),
        "PhoneService": rng.choice(["Yes", "No"], n),
        "MultipleLines": rng.choice(["Yes", "No"], n),
        "InternetService": rng.choice(["DSL", "Fiber optic", "No"], n),
        "OnlineSecurity": rng.choice(["Yes", "No"], n),
        "OnlineBackup": rng.choice(["Yes", "No"], n),
        "DeviceProtection": rng.choice(["Yes", "No"], n),
        "TechSupport": rng.choice(["Yes", "No"], n),
        "StreamingTV": rng.choice(["Yes", "No"], n),
        "StreamingMovies": rng.choice(["Yes", "No"], n),
        "Contract": rng.choice(["Month-to-month", "One year", "Two year"], n),
        "PaperlessBilling": rng.choice(["Yes", "No"], n),
        "PaymentMethod": rng.choice(["Electronic check", "Mailed check"], n),
        "MonthlyCharges": rng.uniform(20, 100, n).round(2),
        # Includes a blank string, matching how the real Kaggle CSV encodes
        # missing TotalCharges for brand-new customers.
        "TotalCharges": [""] + list(rng.uniform(20, 5000, n - 1).round(2)),
        "Churn": rng.choice(["Yes", "No"], n),
    })


# ---------------------------------------------------------------------------
# prepare.clean_and_split
# ---------------------------------------------------------------------------

def test_clean_and_split_drops_customer_id():
    df = _make_fake_raw_df()
    train_df, test_df, _ = clean_and_split(df, test_size=0.25, random_state=42)
    assert "customerID" not in train_df.columns
    assert "customerID" not in test_df.columns


def test_clean_and_split_handles_missing_total_charges():
    df = _make_fake_raw_df()
    train_df, test_df, _ = clean_and_split(df, test_size=0.25, random_state=42)
    combined = pd.concat([train_df, test_df])
    assert combined["TotalCharges"].isnull().sum() == 0


def test_clean_and_split_encodes_categoricals_as_numeric():
    df = _make_fake_raw_df()
    train_df, _, encoders = clean_and_split(df, test_size=0.25, random_state=42)
    assert "Contract" in encoders
    assert pd.api.types.is_numeric_dtype(train_df["Contract"])


def test_clean_and_split_respects_test_size():
    df = _make_fake_raw_df(n=100)
    train_df, test_df, _ = clean_and_split(df, test_size=0.3, random_state=42)
    total = len(train_df) + len(test_df)
    assert total == 100
    assert abs(len(test_df) / total - 0.3) < 0.05


def test_clean_and_split_is_deterministic_given_same_seed():
    df = _make_fake_raw_df()
    train_a, test_a, _ = clean_and_split(df, test_size=0.25, random_state=7)
    train_b, test_b, _ = clean_and_split(df, test_size=0.25, random_state=7)
    pd.testing.assert_frame_equal(train_a, train_b)
    pd.testing.assert_frame_equal(test_a, test_b)


# ---------------------------------------------------------------------------
# train.build_model
# ---------------------------------------------------------------------------

def test_build_model_returns_correct_class():
    assert isinstance(build_model("logistic_regression", {}, 42), LogisticRegression)
    assert isinstance(build_model("random_forest", {}, 42), RandomForestClassifier)
    assert isinstance(build_model("gradient_boosting", {}, 42), GradientBoostingClassifier)


def test_build_model_applies_hyperparameters():
    model = build_model("random_forest", {"n_estimators": 17, "max_depth": 4}, 42)
    assert model.n_estimators == 17
    assert model.max_depth == 4


def test_build_model_sets_random_state():
    model = build_model("gradient_boosting", {}, random_state=99)
    assert model.random_state == 99


def test_build_model_rejects_unknown_model_name():
    try:
        build_model("not_a_real_model", {}, 42)
        assert False, "expected a ValueError for an unknown model name"
    except ValueError:
        pass


# ---------------------------------------------------------------------------
# train.compute_metrics
# ---------------------------------------------------------------------------

def test_compute_metrics_perfect_predictions():
    y_true = [0, 0, 1, 1]
    preds = [0, 0, 1, 1]
    proba = [0.05, 0.1, 0.9, 0.95]
    metrics = compute_metrics(y_true, preds, proba)
    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["roc_auc"] == 1.0
    assert metrics["decision_threshold"] == 0.5


def test_compute_metrics_includes_all_expected_keys():
    y_true = [0, 1, 0, 1]
    preds = [0, 1, 1, 1]
    proba = [0.2, 0.8, 0.6, 0.7]
    metrics = compute_metrics(y_true, preds, proba)
    for key in ["decision_threshold", "accuracy", "precision", "recall", "f1_score", "roc_auc"]:
        assert key in metrics

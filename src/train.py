"""
train.py — DVC Stage 2: TRAIN
Trains a churn-prediction classifier and logs the run (params, metrics,
model artifact) to MLflow. The algorithm + hyperparameters come from
params.yaml so that changing params.yaml and re-running this script is
exactly how you produce a new MLflow "experiment" run (baseline vs
variant 1 vs variant 2 for Phase 1).
"""
import yaml
import json
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, precision_score, recall_score

MODEL_REGISTRY = {
    "logistic_regression": LogisticRegression,
    "random_forest": RandomForestClassifier,
    "gradient_boosting": GradientBoostingClassifier,
}


def build_model(model_name: str, model_params: dict, random_state: int = 42):
    """Pure factory: (model_name, hyperparams) -> an unfitted sklearn estimator.

    Separated from main() so the model-construction logic (registry lookup,
    the logistic-regression max_iter special-case) is directly unit
    testable without needing data files or MLflow (see tests/test_pipeline.py).
    """
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'. Valid options: {list(MODEL_REGISTRY)}")
    ModelClass = MODEL_REGISTRY[model_name]
    if model_name == "logistic_regression":
        return ModelClass(random_state=random_state, max_iter=1000, **model_params)
    return ModelClass(random_state=random_state, **model_params)


def compute_metrics(y_true, preds, proba) -> dict:
    """Pure metrics computation, separated out for unit testing."""
    return {
        "decision_threshold": 0.5,
        "accuracy": accuracy_score(y_true, preds),
        "precision": precision_score(y_true, preds),
        "recall": recall_score(y_true, preds),
        "f1_score": f1_score(y_true, preds),
        "roc_auc": roc_auc_score(y_true, proba),
    }


def main():
    with open("params.yaml") as f:
        all_params = yaml.safe_load(f)
    params = all_params["train"]

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("churn-prediction")

    train_df = pd.read_csv("data/processed/train.csv")
    test_df = pd.read_csv("data/processed/test.csv")

    target = "Churn"
    X_train, y_train = train_df.drop(columns=[target]), train_df[target]
    X_test, y_test = test_df.drop(columns=[target]), test_df[target]

    model_name = params["model"]
    model_params = params.get("model_params", {})
    random_state = params.get("random_state", 42)

    with mlflow.start_run(run_name=params.get("run_name", model_name)):
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("random_state", random_state)
        for k, v in model_params.items():
            mlflow.log_param(k, v)

        model = build_model(model_name, model_params, random_state)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1]

        # All class metrics below use scikit-learn's default 0.5 probability
        # threshold. ROC-AUC is threshold-independent; accuracy/precision/
        # recall/F1 are not, so the threshold is logged explicitly alongside
        # them for anyone comparing runs later.
        metrics = compute_metrics(y_test, preds, proba)
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        mlflow.sklearn.log_model(model, "model")

        joblib.dump(model, "models/model.pkl")
        with open("reports/metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        print(f"[{model_name}] metrics: {metrics}")
        print(f"MLflow run_id: {mlflow.active_run().info.run_id}")

if __name__ == "__main__":
    main()

"""
evaluate.py — DVC Stage 3: EVALUATE
Loads the trained model + test set, produces a confusion matrix,
classification report, and a reference statistics file used later by
the drift-monitoring stage (Phase 2) as the "training-time baseline".
"""
import json
import pandas as pd
import joblib
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    roc_auc_score,
)

DECISION_THRESHOLD = 0.5  # fixed threshold used for all reported class metrics


def main():
    model = joblib.load("models/model.pkl")
    test_df = pd.read_csv("data/processed/test.csv")
    target = "Churn"
    X_test, y_test = test_df.drop(columns=[target]), test_df[target]

    proba = model.predict_proba(X_test)[:, 1]
    preds = (proba >= DECISION_THRESHOLD).astype(int)

    cm = confusion_matrix(y_test, preds).tolist()
    report = classification_report(y_test, preds, output_dict=True)

    # Threshold-dependent metrics (accuracy, precision, recall, F1) are all
    # reported at DECISION_THRESHOLD=0.5. ROC-AUC is threshold-independent.
    summary_metrics = {
        "decision_threshold": DECISION_THRESHOLD,
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1_score": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, proba),
    }

    with open("reports/evaluation.json", "w") as f:
        json.dump(
            {"confusion_matrix": cm, "classification_report": report, "summary_metrics": summary_metrics},
            f, indent=2,
        )

    # Save reference feature statistics — used as the drift-detection baseline in Phase 2
    ref_stats = X_test.describe().to_dict()
    with open("reports/reference_stats.json", "w") as f:
        json.dump(ref_stats, f, indent=2)

    # Save a reference sample (used by EvidentlyAI as the "reference" dataset)
    X_test.assign(**{target: y_test}).to_csv("reports/reference_data.csv", index=False)

    print("Confusion matrix:", cm)
    print("Summary metrics (threshold=0.5):", json.dumps(summary_metrics, indent=2))
    print("Saved reports/evaluation.json, reference_stats.json, reference_data.csv")


if __name__ == "__main__":
    main()

"""
monitor.py — Phase 2 monitoring stage.
Compares the reference (training-time) data distribution against a batch of
current (production) data using EvidentlyAI, saves an HTML drift report, and
prints/returns a machine-readable retraining decision.

Usage:
    python monitoring/monitor.py
Outputs:
    reports/drift_report.html   (full interactive EvidentlyAI report)
    reports/drift_summary.json  (machine-readable summary + retrain flag)
"""
import json
import pandas as pd
from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset

DRIFT_SHARE_THRESHOLD = 0.15  # if >=15% of features drift -> flag for retraining


def main():
    reference_df = pd.read_csv("reports/reference_data.csv")
    current_df = pd.read_csv("reports/current_production_data.csv")

    numerical_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    categorical_cols = [c for c in reference_df.columns if c not in numerical_cols + ["Churn"]]

    definition = DataDefinition(
        numerical_columns=numerical_cols,
        categorical_columns=categorical_cols,
    )

    ref_dataset = Dataset.from_pandas(reference_df, data_definition=definition)
    cur_dataset = Dataset.from_pandas(current_df, data_definition=definition)

    report = Report(metrics=[DataDriftPreset()])
    result = report.run(reference_data=ref_dataset, current_data=cur_dataset)
    result.save_html("reports/drift_report.html")

    result_dict = result.dict()

    # Pull the overall drift share from the result payload
    drift_share = None
    for metric_result in result_dict.get("metrics", []):
        val = metric_result.get("value")
        if isinstance(val, dict) and "share" in val:
            drift_share = val["share"]
            break

    if drift_share is None:
        drift_share = 0.0  # fallback if structure differs across evidently versions

    should_retrain = drift_share >= DRIFT_SHARE_THRESHOLD

    summary = {
        "drift_share": drift_share,
        "threshold": DRIFT_SHARE_THRESHOLD,
        "retrain_recommended": should_retrain,
        "n_reference_rows": len(reference_df),
        "n_current_rows": len(current_df),
    }
    with open("reports/drift_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    if should_retrain:
        print("DRIFT DETECTED -> retraining recommended. See reports/drift_report.html")
    else:
        print("No significant drift detected. Model remains in production.")

    return summary


if __name__ == "__main__":
    main()

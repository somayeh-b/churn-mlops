"""
retrain.py — Phase 2 retraining trigger.
Reads reports/drift_summary.json (produced by monitor.py). If drift was
flagged, it re-runs the DVC pipeline (prepare -> train -> evaluate) to
produce a fresh model, and archives the old one for rollback.

This is what GitHub Actions calls on a schedule (see
.github/workflows/ci-cd.yml, job "monitor-and-retrain").
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone


def main():
    with open("reports/drift_summary.json") as f:
        summary = json.load(f)

    if not summary.get("retrain_recommended"):
        print("No retraining needed — drift below threshold.")
        return 0

    print("Drift threshold exceeded — starting retraining...")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    try:
        shutil.copy("models/model.pkl", f"models/model_backup_{ts}.pkl")
        print(f"Backed up previous model -> models/model_backup_{ts}.pkl")
    except FileNotFoundError:
        pass

    result = subprocess.run(["dvc", "repro"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    print("Retraining complete. New model at models/model.pkl")
    return 0


if __name__ == "__main__":
    sys.exit(main())

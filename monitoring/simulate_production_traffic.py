"""
simulate_production_traffic.py
--------------------------------
Generates a batch of "current" customer data that intentionally drifts from
the training-time reference distribution (reports/reference_data.csv),
so the drift-detection stage (monitor.py) has something real to detect.

In a real deployment this file would instead be built from logged
prediction requests collected by the FastAPI service in production.
Simulating it here keeps Phase 2's monitoring demo fully reproducible
without needing a live traffic history.
"""
import numpy as np
import pandas as pd

np.random.seed(123)


def simulate(n=1500, drift=True):
    ref = pd.read_csv("reports/reference_data.csv")
    sample = ref.sample(n=n, replace=True, random_state=123).reset_index(drop=True)

    if drift:
        # Simulate a realistic drift scenario: a marketing campaign shifted
        # more customers onto Fiber optic + Month-to-month + higher charges,
        # and average tenure of new sign-ups is lower.
        sample["tenure"] = (sample["tenure"] * 0.55).clip(0, 72).astype(int)
        sample["MonthlyCharges"] = sample["MonthlyCharges"] * np.random.uniform(1.15, 1.35, n)
        sample["TotalCharges"] = sample["MonthlyCharges"] * sample["tenure"] + np.random.normal(0, 10, n)

    return sample


if __name__ == "__main__":
    df = simulate(n=1500, drift=True)
    df.to_csv("reports/current_production_data.csv", index=False)
    print(f"Simulated {len(df)} production rows -> reports/current_production_data.csv")

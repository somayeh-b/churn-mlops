"""
generate_dataset.py
--------------------
Generates a SYNTHETIC customer-churn dataset that mimics the structure and
statistical patterns of the well-known IBM/Kaggle "Telco Customer Churn"
dataset (7,043 rows, 21 columns). This is NOT scraped or copied real data —
it is simulated from realistic distributions and business logic so the
MLOps pipeline (DVC, MLflow, FastAPI, monitoring) can be built and tested
end-to-end without needing external internet access to Kaggle.

IMPORTANT (documented honestly in the project proposal / dataset card):
This dataset is synthetic. If your instructor requires a real external
dataset, download the real Telco Customer Churn CSV from Kaggle/IBM and
replace data/raw/churn.csv with it — the pipeline code does not need to
change since column names match the real dataset's schema.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 7043  # same size as the real Telco Churn dataset


def generate():
    customer_id = [
        f"{np.random.randint(1000, 9999)}-{''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 5))}"
        for _ in range(N)
    ]
    gender = np.random.choice(["Male", "Female"], N)
    senior_citizen = np.random.choice([0, 1], N, p=[0.84, 0.16])
    partner = np.random.choice(["Yes", "No"], N, p=[0.48, 0.52])
    dependents = np.random.choice(["Yes", "No"], N, p=[0.3, 0.7])
    tenure = np.random.randint(0, 73, N)

    phone_service = np.random.choice(["Yes", "No"], N, p=[0.9, 0.1])
    multiple_lines = np.where(
        phone_service == "No",
        "No phone service",
        np.random.choice(["Yes", "No"], N, p=[0.42, 0.58]),
    )
    internet_service = np.random.choice(
        ["DSL", "Fiber optic", "No"], N, p=[0.34, 0.44, 0.22]
    )

    def dep_internet(col_yes_p):
        return np.where(
            internet_service == "No",
            "No internet service",
            np.random.choice(["Yes", "No"], N, p=[col_yes_p, 1 - col_yes_p]),
        )

    online_security = dep_internet(0.29)
    online_backup = dep_internet(0.34)
    device_protection = dep_internet(0.34)
    tech_support = dep_internet(0.29)
    streaming_tv = dep_internet(0.38)
    streaming_movies = dep_internet(0.39)

    contract = np.random.choice(
        ["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.21, 0.24]
    )
    paperless_billing = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])
    payment_method = np.random.choice(
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
        ],
        N,
        p=[0.34, 0.23, 0.22, 0.21],
    )

    base_charge = 18.25 + (internet_service != "No") * np.random.uniform(20, 55, N)
    base_charge += (streaming_tv == "Yes") * np.random.uniform(5, 12, N)
    base_charge += (streaming_movies == "Yes") * np.random.uniform(5, 12, N)
    base_charge += (phone_service == "Yes") * np.random.uniform(5, 15, N)
    monthly_charges = np.round(base_charge, 2)
    total_charges = np.round(
        monthly_charges * tenure + np.random.normal(0, 15, N).clip(-50, 50), 2
    )
    total_charges = np.clip(total_charges, 0, None)

    # Business logic driving churn probability (so the model has real signal to learn)
    churn_score = (
        (contract == "Month-to-month") * 0.35
        + (contract == "One year") * 0.10
        - (contract == "Two year") * 0.05
        + (internet_service == "Fiber optic") * 0.15
        + (tech_support == "No") * 0.10
        + (online_security == "No") * 0.08
        + (payment_method == "Electronic check") * 0.12
        - (tenure / 72) * 0.45
        + (monthly_charges / 120) * 0.15
        + (senior_citizen == 1) * 0.05
        - (partner == "Yes") * 0.05
        - (dependents == "Yes") * 0.05
        + np.random.normal(0, 0.12, N)
    )
    churn_prob = 1 / (1 + np.exp(-8 * (churn_score - 0.35)))
    churn = np.where(np.random.uniform(0, 1, N) < churn_prob, "Yes", "No")

    df = pd.DataFrame(
        {
            "customerID": customer_id,
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "Churn": churn,
        }
    )
    return df


if __name__ == "__main__":
    df = generate()
    df.to_csv("data/raw/churn.csv", index=False)
    print(f"Generated {len(df)} rows -> data/raw/churn.csv")
    print(f"Churn rate: {(df['Churn'] == 'Yes').mean():.2%}")

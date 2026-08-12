"""
Unit/integration tests run by CI (see .github/workflows/ci-cd.yml).
Uses FastAPI's TestClient — no real server/network needed.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from app import app

# Use as a context manager so FastAPI's lifespan startup (which loads the
# model/encoders) actually fires before the tests run.
client = TestClient(app)
client.__enter__()  # triggers lifespan startup; process exit cleans it up

VALID_PAYLOAD = {
    "gender": "Female", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
    "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
    "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "Yes", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Two year", "PaperlessBilling": "No",
    "PaymentMethod": "Mailed check", "MonthlyCharges": 55.5, "TotalCharges": 666.0,
}

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_valid_payload():
    r = client.post("/predict", json=VALID_PAYLOAD)
    assert r.status_code == 200
    body = r.json()
    assert body["churn_prediction"] in ("Yes", "No")
    assert 0.0 <= body["churn_probability"] <= 1.0

def test_predict_rejects_invalid_category():
    bad = VALID_PAYLOAD.copy()
    bad["Contract"] = "Three year"  # not a valid category
    r = client.post("/predict", json=bad)
    assert r.status_code == 422

def test_predict_rejects_missing_field():
    bad = VALID_PAYLOAD.copy()
    del bad["tenure"]
    r = client.post("/predict", json=bad)
    assert r.status_code == 422

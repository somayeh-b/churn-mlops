"""
app.py — FastAPI serving layer for Phase 2.
Exposes:
  GET  /            -> health check
  GET  /health      -> health check (used by Docker/cloud health probes)
  POST /predict     -> churn prediction for a single customer
  GET  /model-info  -> which model/version is currently loaded
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from typing import Literal
import joblib
import pandas as pd
import os

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
ENCODERS_PATH = os.getenv("ENCODERS_PATH", "models/label_encoders.pkl")

model = None
encoders = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, encoders
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    yield

app = FastAPI(
    title="Customer Churn Prediction API",
    description="MLOps Project Phase 2 — serves a gradient boosting churn classifier",
    version="1.0.0",
    lifespan=lifespan,
)

FEATURE_ORDER = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges",
]

class CustomerFeatures(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal[0, 1]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int = Field(ge=0, le=100)
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["Yes", "No", "No internet service"]
    OnlineBackup: Literal["Yes", "No", "No internet service"]
    DeviceProtection: Literal["Yes", "No", "No internet service"]
    TechSupport: Literal["Yes", "No", "No internet service"]
    StreamingTV: Literal["Yes", "No", "No internet service"]
    StreamingMovies: Literal["Yes", "No", "No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)

class PredictionResponse(BaseModel):
    churn_prediction: Literal["Yes", "No"]
    churn_probability: float
    model_version: str

@app.get("/")
def root():
    return {"message": "Customer Churn Prediction API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/model-info")
def model_info():
    return {
        "model_type": type(model).__name__ if model else None,
        "n_features": len(FEATURE_ORDER),
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    if model is None or encoders is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    row = customer.model_dump()
    df = pd.DataFrame([row])[FEATURE_ORDER]

    for col, le in encoders.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col])
            except ValueError:
                raise HTTPException(status_code=422, detail=f"Unseen category in field '{col}'")

    proba = model.predict_proba(df)[0, 1]
    pred = "Yes" if proba >= 0.5 else "No"

    return PredictionResponse(
        churn_prediction=pred,
        churn_probability=round(float(proba), 4),
        model_version="gradient_boosting_v1",
    )

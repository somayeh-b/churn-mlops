import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# تعریف کامل تمام ویژگی‌های مورد نیاز مدل
class CustomerData(BaseModel):
    gender: int               # 0: Female, 1: Male (یا برعکس طبق کدگذاری داده)
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: int
    PhoneService: int
    MultipleLines: int
    InternetService: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    Contract: int
    PaperlessBilling: int
    PaymentMethod: int
    MonthlyCharges: float
    TotalCharges: float

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn",
    version="1.0.0"
)

MODEL_PATH = os.path.join("models", "model.pkl")

@app.get("/")
def home():
    return {"message": "Churn Prediction API is up and running!"}

@app.post("/predict")
def predict(data: CustomerData):
    try:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=500, detail=f"Model file not found at {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        input_dict = data.dict()

        # تطبیق ترتیب دقیق ستون‌ها با مدل
        if hasattr(model, "feature_names_in_"):
            required_features = list(model.feature_names_in_)
            input_df = pd.DataFrame([input_dict])[required_features]
        else:
            input_df = pd.DataFrame([input_dict])

        prediction = model.predict(input_df)[0]
        
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_df)[0][1]
            prob_value = round(float(probability), 4)
        else:
            prob_value = None

        return {
            "churn_prediction": int(prediction),
            "churn_probability": prob_value,
            "status": "Churn Risk" if prediction == 1 else "No Churn Risk"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
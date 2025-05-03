from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from typing import Optional
import os
import logging
from backend.utils.preprocessing import preprocess_input  # Updated import

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "model.pkl")
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

class PatientData(BaseModel):
    age: int = Field(..., example=63, description="Age in years")
    sex: int = Field(..., example=1, description="Sex (1 = male, 0 = female)")
    cp: int = Field(..., example=3, description="Chest pain type (0-3)")
    trestbps: int = Field(..., example=145, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., example=233, description="Serum cholesterol (mg/dl)")
    fbs: int = Field(..., example=1, description="Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)")
    restecg: int = Field(..., example=0, description="Resting ECG results (0-2)")
    thalach: int = Field(..., example=150, description="Maximum heart rate achieved")
    exang: int = Field(..., example=0, description="Exercise induced angina (1 = yes, 0 = no)")
    oldpeak: float = Field(..., example=2.3, description="ST depression induced by exercise")
    slope: int = Field(..., example=0, description="Slope of the peak exercise ST segment (0-2)")
    ca: int = Field(..., example=0, description="Number of major vessels colored by fluoroscopy (0-3)")
    thal: int = Field(..., example=1, description="Thalassemia (0 = normal, 1 = fixed defect, 2 = reversible defect)")

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str

def calculate_risk_level(probability: float) -> str:
    """
    Determine the risk level based on the probability.
    """
    if probability >= 0.7:
        return "High"
    elif probability >= 0.3:
        return "Medium"
    else:
        return "Low"

@router.post("/", response_model=PredictionResponse)
async def predict(patient_data: PatientData):
    """
    Predict the risk of heart disease based on patient data.
    """
    if model is None:
        logger.error("Model not loaded.")
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([patient_data.dict()])
        logger.info(f"Received input data: {input_df.to_dict(orient='records')}")

        # Preprocess the input data
        processed_input = preprocess_input(input_df)
        logger.info("Input data preprocessed successfully.")

        # Make prediction
        probability = model.predict_proba(processed_input)[0, 1]
        prediction = 1 if probability >= 0.5 else 0
        logger.info(f"Prediction made: {prediction}, Probability: {probability}")

        # Determine risk level
        risk_level = calculate_risk_level(probability)
        logger.info(f"Risk level determined: {risk_level}")

        return {
            "prediction": prediction,
            "probability": float(probability),
            "risk_level": risk_level
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
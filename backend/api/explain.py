from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import shap
import lime
import lime.lime_tabular
from typing import List, Dict, Any
import os
import json
from backend.api.predict import PatientData  # Corrected import
from backend.utils.preprocessing import preprocess_input  # Corrected import

router = APIRouter()

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "model.pkl")
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Initialize SHAP explainer (global initialization for tree-based models)
shap_explainer = None
if model:
    try:
        shap_explainer = shap.Explainer(model)
    except Exception as e:
        print(f"Error initializing SHAP explainer: {e}")

class FeatureImportance(BaseModel):
    feature: str
    importance: float
    direction: str  # "positive" or "negative"

class ExplanationResponse(BaseModel):
    prediction: int
    probability: float
    shap_values: List[Dict[str, float]]
    feature_importance: List[FeatureImportance]
    lime_explanation: Dict[str, Any]

@router.post("/", response_model=ExplanationResponse)
async def explain_prediction(patient_data: PatientData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([patient_data.dict()])
        feature_names = list(input_df.columns)
        
        # Preprocess the input data
        processed_input = preprocess_input(input_df)
        
        # Make prediction
        probability = model.predict_proba(processed_input)[0, 1]
        prediction = 1 if probability >= 0.5 else 0
        
        # Generate SHAP explanation
        if shap_explainer is None:
            raise HTTPException(status_code=500, detail="SHAP explainer not initialized")
        
        shap_values = shap_explainer(processed_input)
        
        # Format SHAP values for response
        formatted_shap = [
            {"feature": feature, "value": float(shap_values.values[0][i])}
            for i, feature in enumerate(feature_names)
        ]
        
        # Feature importance (using absolute SHAP values)
        feature_importance = [
            FeatureImportance(
                feature=feature,
                importance=float(abs(shap_values.values[0][i])),
                direction="positive" if shap_values.values[0][i] > 0 else "negative"
            )
            for i, feature in enumerate(feature_names)
        ]
        
        # Sort feature importance by absolute value
        feature_importance.sort(key=lambda x: x.importance, reverse=True)
        
        # Generate LIME explanation
        lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=np.array(processed_input),
            feature_names=feature_names,
            class_names=["No Disease", "Disease"],
            mode="classification"
        )
        
        lime_exp = lime_explainer.explain_instance(
            processed_input.iloc[0].values, 
            model.predict_proba,
            num_features=10
        )
        
        # Format LIME explanation
        lime_explanation = {
            "intercept": lime_exp.intercept,
            "features": [{"feature": feature, "weight": weight} 
                         for feature, weight in lime_exp.as_list()]
        }
        
        return {
            "prediction": prediction,
            "probability": float(probability),
            "shap_values": formatted_shap,
            "feature_importance": feature_importance,
            "lime_explanation": lime_explanation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation error: {str(e)}")
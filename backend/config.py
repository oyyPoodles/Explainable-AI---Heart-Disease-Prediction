"""
Configuration settings for the Heart Disease Prediction application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data paths
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR.parent / "data"))
HEART_DATA_PATH = DATA_DIR / "heart.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Model paths
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "model"))
MODEL_PATH = MODEL_DIR / "model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
FEATURE_NAMES_PATH = MODEL_DIR / "feature_names.pkl"
BACKGROUND_DATA_PATH = MODEL_DIR / "background_data.pkl"

# Ensure critical directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# API settings
API_TITLE = "Heart Disease Prediction API"
API_DESCRIPTION = "API for heart disease prediction with explainable AI"
API_VERSION = "1.0.0"
API_PREFIX = "/api"

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",  # React app
    "http://localhost:8000",  # FastAPI server
    "*"  # Allow all origins in development (remove in production)
]

# Feature descriptions (for explanation purposes)
FEATURE_DESCRIPTIONS = {
    "age": "Age in years",
    "sex": "Sex (1 = male, 0 = female)",
    "cp": "Chest pain type (0-3)",
    "trestbps": "Resting blood pressure in mm Hg",
    "chol": "Serum cholesterol in mg/dl",
    "fbs": "Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)",
    "restecg": "Resting electrocardiographic results (0-2)",
    "thalach": "Maximum heart rate achieved",
    "exang": "Exercise induced angina (1 = yes, 0 = no)",
    "oldpeak": "ST depression induced by exercise relative to rest",
    "slope": "Slope of the peak exercise ST segment (0-2)",
    "ca": "Number of major vessels colored by fluoroscopy (0-3)",
    "thal": "Thalassemia (0 = normal, 1 = fixed defect, 2 = reversible defect)"
}

# Model training settings
RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
VAL_SIZE = float(os.getenv("VAL_SIZE", 0.25))
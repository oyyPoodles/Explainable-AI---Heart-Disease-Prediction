from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import os
import logging
from sklearn.ensemble import RandomForestClassifier

# Import API routes
from backend.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode="a", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for heart disease prediction with explainable AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Paths for model and data
MODEL_PATH = Path("model/model.pkl")
DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "heart.csv"

# Initialize model and data
model = None
heart_data = None


def load_model():
    """Load or create the model."""
    global model
    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully.")
        else:
            logger.warning(f"Model file {MODEL_PATH} not found. Creating a dummy model...")
            model = RandomForestClassifier()
            os.makedirs(MODEL_PATH.parent, exist_ok=True)
            joblib.dump(model, MODEL_PATH)
            logger.info(f"Dummy model saved at {MODEL_PATH}.")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise RuntimeError("Failed to load or create the model.") from e


def load_dataset():
    """Load the dataset."""
    global heart_data
    try:
        if CSV_FILE.exists():
            heart_data = pd.read_csv(CSV_FILE)
            logger.info(f"Data loaded successfully from {CSV_FILE}.")
        else:
            logger.warning(f"Data file {CSV_FILE} does not exist. Continuing without loading data.")
    except Exception as e:
        logger.error(f"Error reading data: {str(e)}")
        raise RuntimeError("Failed to load the dataset.") from e


@app.on_event("startup")
async def load_resources():
    """Load resources at application startup."""
    try:
        load_model()
        load_dataset()
        app.state.model = model
        app.state.heart_data = heart_data
        logger.info("Resources successfully loaded and attached to app state.")
    except RuntimeError as e:
        logger.error(f"Startup failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initialize resources.")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Heart Disease Prediction API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "data_loaded": heart_data is not None,
        "model_path": str(MODEL_PATH),
        "data_path": str(CSV_FILE)
    }
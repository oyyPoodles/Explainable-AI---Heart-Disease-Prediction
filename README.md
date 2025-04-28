# Heart Disease XAI Chatbot

An Explainable AI (XAI) application for heart disease risk prediction with transparent explanations.

## Project Overview

This application predicts a patient's risk of heart disease based on clinical features and provides explanations for the predictions using Explainable AI techniques. The system consists of:

- **Machine Learning Backend**: Trained on heart disease data with multiple models (Logistic Regression, Random Forest, XGBoost)
- **XAI Components**: SHAP and LIME explanations for model predictions
- **Interactive Frontend**: User-friendly interface for entering patient data and viewing results
- **API**: RESTful endpoints for predictions and explanations

## Features

- Heart disease risk prediction (Yes/No) with probability score
- Visualization of feature importance (which factors matter most)
- SHAP force plots showing how each feature contributes to a prediction
- LIME explanations for individual predictions
- Responsive frontend for desktop and mobile use

## Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/heart-xai-chatbot.git
cd heart-xai-chatbot

# Start the application with Docker Compose
docker-compose up -d
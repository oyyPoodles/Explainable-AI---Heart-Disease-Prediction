import pandas as pd
import numpy as np
import shap
from lime import lime_tabular

def generate_explanation(patient_data, model, scaler, feature_names, X_scaled):
    """
    Generate SHAP and LIME explanations for a patient's prediction.

    Args:
        patient_data (pd.DataFrame): Patient features as a DataFrame
        model: Trained ML model
        scaler: Feature scaler used during training
        feature_names (list): List of feature names
        X_scaled (np.ndarray): Scaled training data for LIME and SHAP background

    Returns:
        dict: Dictionary containing prediction and explanations
    """
    try:
        # Scale the input data
        patient_data_scaled = scaler.transform(patient_data)

        # Make prediction
        prediction = model.predict(patient_data_scaled)[0]
        probability = model.predict_proba(patient_data_scaled)[0, 1]

        # Initialize SHAP explainer
        try:
            if hasattr(model, 'feature_importances_'):
                explainer = shap.TreeExplainer(model)
            else:
                # Use a subset of the training data as background
                background_data = shap.sample(X_scaled, 100)
                explainer = shap.KernelExplainer(model.predict_proba, background_data)
        except Exception as e:
            raise ValueError(f"Error initializing SHAP explainer: {e}")

        # Calculate SHAP values
        shap_values = explainer.shap_values(patient_data_scaled)

        # For binary classification, some models return a list
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For the positive class

        # Get SHAP values as dictionary
        shap_dict = {feature: float(value) for feature, value in zip(feature_names, shap_values[0])}

        # Initialize LIME explainer
        try:
            lime_explainer = lime_tabular.LimeTabularExplainer(
                X_scaled,
                feature_names=feature_names,
                class_names=['No Heart Disease', 'Heart Disease'],
                mode='classification'
            )

            # Generate LIME explanation
            lime_exp = lime_explainer.explain_instance(
                patient_data_scaled[0],
                model.predict_proba,
                num_features=len(feature_names),
                top_labels=1
            )

            # Extract LIME explanation as list of (feature, weight) tuples
            lime_list = lime_exp.as_list(label=1)
            lime_explanation = [{'feature': item[0], 'weight': float(item[1])} for item in lime_list]
        except Exception as e:
            raise ValueError(f"Error generating LIME explanation: {e}")

        # Get global feature importance if available
        if hasattr(model, 'feature_importances_'):
            feature_importance = {feature: float(importance) 
                                  for feature, importance in zip(feature_names, model.feature_importances_)}
        elif hasattr(model, 'coef_'):
            feature_importance = {feature: float(abs(coef)) 
                                  for feature, coef in zip(feature_names, model.coef_[0])}
        else:
            feature_importance = {feature: 0.0 for feature in feature_names}  # Default to 0 if unavailable

        # Create explanation dictionary
        explanation = {
            'prediction': int(prediction),
            'probability': float(probability),
            'shap_values': shap_dict,
            'feature_importance': feature_importance,
            'lime_explanation': lime_explanation,
            'expected_value': float(explainer.expected_value if not hasattr(explainer, 'expected_value') 
                                  else explainer.expected_value[1])
        }

        return explanation

    except Exception as e:
        raise ValueError(f"Error generating explanation: {e}")
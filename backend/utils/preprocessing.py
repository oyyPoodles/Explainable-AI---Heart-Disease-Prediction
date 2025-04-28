import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(filepath='../../data/heart.csv'):
    """
    Load and preprocess the heart disease dataset.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        X: Features DataFrame
        y: Target Series
        feature_names: List of feature names
    """
    # Load the data
    data = pd.read_csv(filepath)
    
    # Separate features and target
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Store feature names
    feature_names = X.columns.tolist()
    
    # Handle missing values (if any)
    X = X.fillna(X.mean())
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    return X, y, feature_names, scaler

def preprocess_input(input_data):
    """
    Preprocess input data for prediction.
    
    Args:
        input_data: DataFrame containing patient data
        
    Returns:
        Preprocessed DataFrame ready for model prediction
    """
    # Handle missing values
    input_data = input_data.fillna(0)
    
    # Load the scaler (in production, this would be loaded from a saved file)
    # For simplicity, we're recreating it here
    _, _, _, scaler = load_and_preprocess_data()
    
    # Apply scaling to numerical columns
    numerical_cols = input_data.select_dtypes(include=['int64', 'float64']).columns
    input_data[numerical_cols] = scaler.transform(input_data[numerical_cols])
    
    return input_data
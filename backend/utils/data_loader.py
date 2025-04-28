import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

def load_heart_data(data_path):
    """
    Load the heart disease dataset.
    
    Args:
        data_path: Path to the heart disease CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    # Check if file exists
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    # Load data
    try:
        df = pd.read_csv(data_path)
        print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def split_data(df, target_col='target', test_size=0.2, val_size=0.25, random_state=42):
    """
    Split the dataset into training, validation, and test sets.
    
    Args:
        df: Input DataFrame
        target_col: Name of the target column
        test_size: Proportion of data for test set
        val_size: Proportion of training data for validation
        random_state: Random seed for reproducibility
        
    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # First split: training + validation vs test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Second split: training vs validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, 
        test_size=val_size, 
        random_state=random_state,
        stratify=y_train_val
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def save_processed_data(X_train, X_val, X_test, y_train, y_val, y_test, output_dir):
    """
    Save processed datasets to CSV files.
    
    Args:
        X_train, X_val, X_test: Feature sets
        y_train, y_val, y_test: Target sets
        output_dir: Directory to save processed data
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save training data
    train_df = X_train.copy()
    train_df['target'] = y_train.values
    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    
    # Save validation data
    val_df = X_val.copy()
    val_df['target'] = y_val.values
    val_df.to_csv(os.path.join(output_dir, 'val.csv'), index=False)
    
    # Save test data
    test_df = X_test.copy()
    test_df['target'] = y_test.values
    test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)
    
    print(f"Processed datasets saved to {output_dir}")
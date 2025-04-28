import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import load_and_preprocess_data

def train_models(data_path='../../data/heart.csv', model_path='model.pkl'):
    """
    Train multiple models and save the best one.
    
    Args:
        data_path: Path to the heart disease dataset
        model_path: Path to save the best model
    """
    print("Loading and preprocessing data...")
    X, y, feature_names, _ = load_and_preprocess_data(data_path)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Test data shape: {X_test.shape}")
    
    # Initialize models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'XGBoost': xgb.XGBClassifier(random_state=42)
    }
    
    # Parameters for grid search
    param_grids = {
        'Logistic Regression': {
            'C': [0.01, 0.1, 1, 10, 100],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear']
        },
        'Random Forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        },
        'XGBoost': {
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7],
            'n_estimators': [50, 100, 200]
        }
    }
    
    # Train and evaluate models
    best_models = {}
    best_scores = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Perform grid search
        grid_search = GridSearchCV(
            model, param_grids[name], cv=5, scoring='roc_auc', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        # Get best model
        best_model = grid_search.best_estimator_
        best_models[name] = best_model
        
        # Predict on test set
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        best_scores[name] = roc_auc
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Test Precision: {precision:.4f}")
        print(f"Test Recall: {recall:.4f}")
        print(f"Test F1 Score: {f1:.4f}")
        print(f"Test ROC AUC: {roc_auc:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(best_model, X, y, cv=5, scoring='roc_auc')
        print(f"Cross-validation ROC AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # Select the best model based on ROC AUC
    best_model_name = max(best_scores, key=best_scores.get)
    best_model = best_models[best_model_name]
    
    print(f"\nBest model: {best_model_name} with ROC AUC: {best_scores[best_model_name]:.4f}")
    
    # Save the best model
    print(f"Saving best model to {model_path}...")
    joblib.dump(best_model, model_path)
    
    # If the best model is Random Forest or XGBoost, plot feature importance
    if best_model_name in ['Random Forest', 'XGBoost']:
        plt.figure(figsize=(12, 8))
        
        if best_model_name == 'Random Forest':
            importances = best_model.feature_importances_
        else:  # XGBoost
            importances = best_model.feature_importances_
            
        indices = np.argsort(importances)[::-1]
        
        plt.title(f"Feature Importance - {best_model_name}")
        plt.bar(range(X.shape[1]), importances[indices], align='center')
        plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(os.path.dirname(model_path), 'feature_importance.png'))
    
    return best_model, X_test, y_test

if __name__ == "__main__":
    # Determine the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '../../data/heart.csv')
    model_path = os.path.join(script_dir, 'model.pkl')
    
    # Train models
    best_model, X_test, y_test = train_models(data_path, model_path)
    
    print("Model training complete!")
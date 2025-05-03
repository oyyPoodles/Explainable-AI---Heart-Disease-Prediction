import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.model_selection import cross_validate

def evaluate_model(model, X_test, y_test, output_dir=None):
    """
    Evaluate the model performance and generate evaluation metrics.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        output_dir: Directory to save evaluation results (optional)
    
    Returns:
        dict: Dictionary containing evaluation metrics
    """
    try:
        # Predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        # Get confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Get classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Results dictionary
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm.tolist(),
            'classification_report': report
        }
        
        # Save results if output_dir is provided
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save metrics to JSON
            try:
                pd.DataFrame([results]).to_json(
                    os.path.join(output_dir, 'metrics.json'),
                    orient='records'
                )
            except Exception as e:
                print(f"Error saving metrics.json: {e}")
            
            # Plot and save confusion matrix
            try:
                plt.figure(figsize=(8, 6))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                            xticklabels=['No Disease', 'Disease'],
                            yticklabels=['No Disease', 'Disease'])
                plt.xlabel('Predicted')
                plt.ylabel('Actual')
                plt.title('Confusion Matrix')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
                plt.close()
            except Exception as e:
                print(f"Error saving confusion_matrix.png: {e}")
            
            # Plot and save ROC curve
            try:
                plt.figure(figsize=(8, 6))
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
                plt.plot([0, 1], [0, 1], 'k--')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('ROC Curve')
                plt.legend()
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'roc_curve.png'))
                plt.close()
            except Exception as e:
                print(f"Error saving roc_curve.png: {e}")
        
        return results
    
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        return {}

def cross_validate_model(model, X, y, cv=5):
    """
    Perform cross-validation for the model and calculate metrics.
    
    Args:
        model: Model to validate
        X: Features
        y: Labels
        cv: Number of cross-validation folds (default: 5)
        
    Returns:
        dict: Cross-validation results with mean and standard deviation for each metric
    """
    try:
        scoring = {
            'accuracy': 'accuracy',
            'precision': 'precision',
            'recall': 'recall',
            'f1': 'f1',
            'roc_auc': 'roc_auc'
        }
        
        cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring)
        
        results = {
            'accuracy': cv_results['test_accuracy'].mean(),
            'precision': cv_results['test_precision'].mean(),
            'recall': cv_results['test_recall'].mean(),
            'f1': cv_results['test_f1'].mean(),
            'roc_auc': cv_results['test_roc_auc'].mean(),
            'std_accuracy': cv_results['test_accuracy'].std(),
            'std_precision': cv_results['test_precision'].std(),
            'std_recall': cv_results['test_recall'].std(),
            'std_f1': cv_results['test_f1'].std(),
            'std_roc_auc': cv_results['test_roc_auc'].std()
        }
        
        return results
    
    except Exception as e:
        print(f"Error during cross-validation: {e}")
        return {}
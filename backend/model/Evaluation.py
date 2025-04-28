import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib

def evaluate_model(model, X_test, y_test, output_dir=None):
    """
    Evaluate the model performance and generate evaluation metrics.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        output_dir: Directory to save evaluation results
    
    Returns:
        dict: Dictionary containing evaluation metrics
    """
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
    
    # Save results if output_dir provided
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save metrics to JSON
        pd.DataFrame([results]).to_json(
            os.path.join(output_dir, 'metrics.json'),
            orient='records'
        )
        
        # Plot and save confusion matrix
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
        
        # Plot and save ROC curve
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
    
    return results

def roc_curve(y_true, y_pred_prob):
    """
    Generate the ROC curve points.
    
    Args:
        y_true: True labels
        y_pred_prob: Predicted probabilities
        
    Returns:
        tuple: (fpr, tpr, thresholds)
    """
    from sklearn.metrics import roc_curve
    return roc_curve(y_true, y_pred_prob)

def cross_validate_model(model, X, y, cv=5):
    """
    Perform cross-validation for the model.
    
    Args:
        model: Model to validate
        X: Features
        y: Labels
        cv: Number of cross-validation folds
        
    Returns:
        dict: Cross-validation results
    """
    from sklearn.model_selection import cross_validate
    
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
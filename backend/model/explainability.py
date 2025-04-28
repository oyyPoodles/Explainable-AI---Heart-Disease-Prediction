import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import shap
import lime
import lime.lime_tabular
from sklearn.inspection import permutation_importance
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import load_and_preprocess_data

def generate_feature_importance(model, X, feature_names, output_path='feature_importance.png'):
    """
    Generate feature importance plot for tree-based models.
    
    Args:
        model: Trained model (Random Forest or XGBoost)
        X: Feature dataset
        feature_names: List of feature names
        output_path: Path to save the plot
    """
    plt.figure(figsize=(12, 8))
    
    # Check if model has feature_importances_ attribute
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.title("Feature Importance")
        plt.bar(range(X.shape[1]), importances[indices], align='center')
        plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
        plt.tight_layout()
        plt.savefig(output_path)
        
        return pd.DataFrame({
            'Feature': [feature_names[i] for i in indices],
            'Importance': importances[indices]
        })
    else:
        # For models without feature_importances_, use permutation importance
        result = permutation_importance(model, X, y, n_repeats=10, random_state=42)
        importances = result.importances_mean
        indices = np.argsort(importances)[::-1]
        
        plt.title("Permutation Feature Importance")
        plt.bar(range(X.shape[1]), importances[indices], align='center')
        plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
        plt.tight_layout()
        plt.savefig(output_path)
        
        return pd.DataFrame({
            'Feature': [feature_names[i] for i in indices],
            'Importance': importances[indices]
        })

def generate_shap_explanations(model, X, feature_names, output_dir='shap_plots'):
    """
    Generate SHAP explanations for the model.
    
    Args:
        model: Trained model
        X: Feature dataset
        feature_names: List of feature names
        output_dir: Directory to save the plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create SHAP explainer
    explainer = shap.Explainer(model)
    shap_values = explainer(X)
    
    # Summary plot
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'shap_summary.png'))
    plt.close()
    
    # Bar plot
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X, feature_names=feature_names, plot_type='bar', show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'shap_bar.png'))
    plt.close()
    
    # Force plots for a few samples
    for i in range(min(5, X.shape[0])):
        plt.figure(figsize=(16, 3))
        shap.plots.force(shap_values[i], matplotlib=True, show=False)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'shap_force_{i}.png'))
        plt.close()
    
    return shap_values

def generate_lime_explanation(model, X, feature_names, class_names=['No Disease', 'Disease'], sample_index=0, output_path='lime_explanation.png'):
    """
    Generate LIME explanation for a specific sample.
    
    Args:
        model: Trained model
        X: Feature dataset
        feature_names: List of feature names
        class_names: List of class names
        sample_index: Index of the sample to explain
        output_path: Path to save the plot
    """
    # Create LIME explainer
    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=np.array(X),
        feature_names=feature_names,
        class_names=class_names,
        mode='classification'
    )
    
    # Explain a specific instance
    sample = X.iloc[sample_index].values
    explanation = explainer.explain_instance(
        sample, 
        model.predict_proba,
        num_features=10
    )
    
    # Save explanation as figure
    fig = explanation.as_pyplot_figure(label=1)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    
    return explanation

def generate_all_explanations(model_path='model.pkl', data_path='../../data/heart.csv', output_dir='xai_results'):
    """
    Generate all XAI explanations for the model.
    
    Args:
        model_path: Path to the trained model
        data_path: Path to the dataset
        output_dir: Directory to save the explanations
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load model
    model = joblib.load(model_path)
    
    # Load data
    X, y, feature_names, _ = load_and_preprocess_data(data_path)
    
    # Generate feature importance
    feature_importance = generate_feature_importance(
        model, X, feature_names, 
        output_path=os.path.join(output_dir, 'feature_importance.png')
    )
    
    # Generate SHAP explanations
    shap_values = generate_shap_explanations(
        model, X, feature_names,
        output_dir=os.path.join(output_dir, 'shap_plots')
    )
    
    # Generate LIME explanations
    lime_explanation = generate_lime_explanation(
        model, X, feature_names,
        output_path=os.path.join(output_dir, 'lime_explanation.png')
    )
    
    print(f"XAI explanations generated and saved to {output_dir}")
    
    return {
        'feature_importance': feature_importance,
        'shap_values': shap_values,
        'lime_explanation': lime_explanation
    }

if __name__ == "__main__":
    # Determine the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'model.pkl')
    data_path = os.path.join(script_dir, '../../data/heart.csv')
    output_dir = os.path.join(script_dir, 'xai_results')
    
    # Generate explanations
    explanations = generate_all_explanations(model_path, data_path, output_dir)
    
    print("Explainability analysis complete!")
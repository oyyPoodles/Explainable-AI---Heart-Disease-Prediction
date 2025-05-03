import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import shap
from lime import lime_tabular
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def plot_feature_distributions(df, target_col='target', output_dir=None):
    """
    Plot distributions of features by target class.
    
    Args:
        df: DataFrame with features and target.
        target_col: Name of the target column.
        output_dir: Directory to save plots.
    """
    try:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Get feature columns
        feature_cols = [col for col in df.columns if col != target_col]
        
        # Create plots for each feature
        for feature in feature_cols:
            plt.figure(figsize=(10, 6))
            
            if df[feature].nunique() <= 5:  # Categorical feature
                sns.countplot(x=feature, hue=target_col, data=df)
                plt.title(f'Distribution of {feature} by Target')
                plt.xticks(rotation=45)
            else:  # Continuous feature
                sns.histplot(
                    data=df, x=feature, hue=target_col, 
                    kde=True, element="step", common_norm=False,
                    palette=['blue', 'red']
                )
                plt.title(f'Distribution of {feature} by Target')
            
            plt.tight_layout()
            
            if output_dir:
                plt.savefig(os.path.join(output_dir, f'dist_{feature}.png'))
                plt.close()
            else:
                plt.show()
    except Exception as e:
        logger.error(f"Error plotting feature distributions: {str(e)}")
        raise

def plot_correlation_matrix(df, target_col='target', output_dir=None):
    """
    Plot correlation matrix for features.
    
    Args:
        df: DataFrame with features and target.
        target_col: Name of the target column.
        output_dir: Directory to save plot.
    """
    try:
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Plot correlation matrix
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(
            corr_matrix, mask=mask, annot=True, 
            cmap='coolwarm', fmt=".2f", linewidths=0.5
        )
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
            plt.close()
        else:
            plt.show()
    except Exception as e:
        logger.error(f"Error plotting correlation matrix: {str(e)}")
        raise

def plot_shap_summary(shap_values, features, feature_names=None, output_path=None):
    """
    Plot SHAP summary plot.
    
    Args:
        shap_values: SHAP values.
        features: Feature data.
        feature_names: List of feature names.
        output_path: Path to save the plot.
    """
    try:
        plt.figure(figsize=(12, 8))
        shap.summary_plot(
            shap_values, features, 
            feature_names=feature_names,
            show=False
        )
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path)
            plt.close()
        else:
            plt.show()
    except Exception as e:
        logger.error(f"Error plotting SHAP summary: {str(e)}")
        raise

def plot_lime_explanation(explanation, class_index=1, output_path=None):
    """
    Plot LIME explanation.
    
    Args:
        explanation: LIME explanation object.
        class_index: Index of the class to explain.
        output_path: Path to save the plot.
    """
    try:
        plt.figure(figsize=(10, 6))
        explanation.as_pyplot_figure(class_index)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path)
            plt.close()
        else:
            plt.show()
    except Exception as e:
        logger.error(f"Error plotting LIME explanation: {str(e)}")
        raise

def plot_patient_explanation(patient_data, shap_values, feature_names, output_path=None):
    """
    Create a custom visualization for a patient's prediction explanation.
    
    Args:
        patient_data: Patient's feature values.
        shap_values: SHAP values for the patient.
        feature_names: List of feature names.
        output_path: Path to save the plot.
    """
    try:
        # Sort features by SHAP value magnitude
        feature_importance = [(name, abs(val)) for name, val in zip(feature_names, shap_values)]
        sorted_features = sorted(feature_importance, key=lambda x: x[1], reverse=True)
        
        # Get top 10 features
        top_features = sorted_features[:10]
        
        # Extract names and values
        names = [f[0] for f in top_features]
        values = [shap_values[feature_names.index(f[0])] for f in top_features]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        colors = ['red' if v < 0 else 'green' for v in values]
        plt.barh(names, values, color=colors)
        plt.xlabel('SHAP value (impact on prediction)')
        plt.title('Top Features Affecting Prediction')
        plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path)
            plt.close()
        else:
            plt.show()
    except Exception as e:
        logger.error(f"Error plotting patient explanation: {str(e)}")
        raise
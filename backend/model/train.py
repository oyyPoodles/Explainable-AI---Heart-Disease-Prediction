import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import joblib
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data():
    """Load and prepare the heart disease dataset."""
    try:
        processed_dir = Path("C:/Users/DELL/Desktop/heart-xai-chatbot/data/processed")
        encoders_dir = Path("C:/Users/DELL/Desktop/heart-xai-chatbot/backend/model/encoders")
        encoders_dir.mkdir(parents=True, exist_ok=True)

        if (processed_dir / "X_train.csv").exists():
            logger.info("Loading processed data...")
            X_train = pd.read_csv(processed_dir / "X_train.csv")
            X_test = pd.read_csv(processed_dir / "X_test.csv")
            y_train = pd.read_csv(processed_dir / "y_train.csv").values.ravel()
            y_test = pd.read_csv(processed_dir / "y_test.csv").values.ravel()
            return X_train, X_test, y_train, y_test

        logger.info("Loading raw data...")
        data_path = Path("../data/heart.csv")
        if not data_path.exists():
            logger.error(f"Data file not found: {data_path}")
            return create_dummy_dataset()

        data = pd.read_csv(data_path)

        feature_names = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                         'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']

        X = data[feature_names]
        y = data['HeartDisease']

        # Encode categorical columns
        categorical_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            joblib.dump(le, encoders_dir / f"{col}_encoder.pkl")  # Save encoder

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        os.makedirs(processed_dir, exist_ok=True)
        X_train.to_csv(processed_dir / "X_train.csv", index=False)
        X_test.to_csv(processed_dir / "X_test.csv", index=False)
        pd.DataFrame(y_train).to_csv(processed_dir / "y_train.csv", index=False)
        pd.DataFrame(y_test).to_csv(processed_dir / "y_test.csv", index=False)

        return X_train, X_test, y_train, y_test

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return create_dummy_dataset()

def create_dummy_dataset():
    """Create a simple dummy dataset for testing when real data is not available."""
    features = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']
    
    np.random.seed(42)
    n_samples = 100
    X = pd.DataFrame(np.random.rand(n_samples, len(features)), columns=features)
    y = np.random.randint(0, 2, size=n_samples)
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """Train a machine learning model for heart disease prediction."""
    try:
        logger.info("Training model...")

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        param_grid = {
            'classifier__n_estimators': [50, 100],
            'classifier__max_depth': [10, 20]
        }

        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_

        logger.info(f"Best hyperparameters: {grid_search.best_params_}")
        return best_model

    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        logger.info("Using default RandomForestClassifier")

        fallback_model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=42))
        ])
        fallback_model.fit(X_train, y_train)
        return fallback_model

def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model."""
    try:
        logger.info("Evaluating model...")

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)

        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info(f"ROC AUC: {roc_auc:.4f}")
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred))

        return accuracy, roc_auc

    except Exception as e:
        logger.error(f"Error evaluating model: {str(e)}")
        return 0, 0

def save_model(model):
    """Save the trained model to disk."""
    try:
        model_dir = Path("model")
        model_dir.mkdir(exist_ok=True)

        model_path = model_dir / "model.pkl"
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")

    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")

def main():
    """Main function to train and save the heart disease prediction model."""
    logger.info("Starting model training process...")

    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    save_model(model)

    logger.info("Model training process completed.")

if __name__ == "__main__":
    main()
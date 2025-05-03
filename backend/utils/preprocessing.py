import pandas as pd
import os
import logging
from sklearn.model_selection import train_test_split
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define default paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DATA_PATH = DATA_DIR / "heart.csv"

def load_heart_data(data_path=None):
    """
    Load the heart disease dataset.

    Args:
        data_path (str or Path, optional): Path to the heart disease CSV file.
                                           Defaults to DEFAULT_DATA_PATH.

    Returns:
        pd.DataFrame: Loaded dataset.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If there is an error reading the file.
    """
    if data_path is None:
        data_path = DEFAULT_DATA_PATH

    data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    try:
        df = pd.read_csv(data_path)
        logger.info(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns from {data_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {data_path}: {str(e)}")
        raise

def split_data(df, target_col='target', test_size=0.2, val_size=0.25, random_state=42):
    """
    Split the dataset into training, validation, and test sets.

    Args:
        df (pd.DataFrame): Input DataFrame.
        target_col (str): Name of the target column.
        test_size (float): Proportion of data for the test set.
        val_size (float): Proportion of training data for validation.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test).

    Raises:
        ValueError: If the input DataFrame is invalid or target column is missing.
        Exception: If there is an error during splitting.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")

    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in the DataFrame.")

    try:
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

        logger.info(f"Training set: {X_train.shape[0]} samples")
        logger.info(f"Validation set: {X_val.shape[0]} samples")
        logger.info(f"Test set: {X_test.shape[0]} samples")

        return X_train, X_val, X_test, y_train, y_val, y_test
    except Exception as e:
        logger.error(f"Error splitting data: {str(e)}")
        raise

def save_processed_data(X_train, X_val, X_test, y_train, y_val, y_test, output_dir=None):
    """
    Save processed datasets to CSV files.

    Args:
        X_train, X_val, X_test (pd.DataFrame): Feature sets.
        y_train, y_val, y_test (pd.Series): Target sets.
        output_dir (str or Path, optional): Directory to save processed data.
                                            Defaults to DATA_DIR / "processed".

    Raises:
        ValueError: If the output directory is invalid.
        Exception: If there is an error saving the data.
    """
    if output_dir is None:
        output_dir = DATA_DIR / "processed"

    output_dir = Path(output_dir)

    try:
        os.makedirs(output_dir, exist_ok=True)

        # Save training data
        train_df = X_train.copy()
        train_df['target'] = y_train.values
        train_df.to_csv(output_dir / 'train.csv', index=False)
        logger.info("Training data saved successfully.")

        # Save validation data
        val_df = X_val.copy()
        val_df['target'] = y_val.values
        val_df.to_csv(output_dir / 'val.csv', index=False)
        logger.info("Validation data saved successfully.")

        # Save test data
        test_df = X_test.copy()
        test_df['target'] = y_test.values
        test_df.to_csv(output_dir / 'test.csv', index=False)
        logger.info("Test data saved successfully.")

        logger.info(f"Processed datasets saved to {output_dir}")
    except Exception as e:
        logger.error(f"Error saving processed data: {str(e)}")
        raise
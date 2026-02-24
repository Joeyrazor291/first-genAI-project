"""Dataset ingestion module - loads data from Hugging Face."""

import logging
from typing import Optional
import pandas as pd
from datasets import load_dataset

from src.config import DATASET_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_restaurant_dataset(dataset_name: Optional[str] = None) -> pd.DataFrame:
    """
    Load the Zomato restaurant dataset from Hugging Face.
    
    Args:
        dataset_name: Name of the Hugging Face dataset. Defaults to config value.
        
    Returns:
        DataFrame containing the raw restaurant data.
        
    Raises:
        Exception: If dataset loading fails.
    """
    dataset_name = dataset_name or DATASET_NAME
    
    try:
        logger.info(f"Loading dataset: {dataset_name}")
        dataset = load_dataset(dataset_name)
        
        # Convert to pandas DataFrame
        # Assuming the dataset has a 'train' split, adjust if needed
        if 'train' in dataset:
            df = dataset['train'].to_pandas()
        else:
            # If no split, try to get the first available split
            split_name = list(dataset.keys())[0]
            df = dataset[split_name].to_pandas()
        
        logger.info(f"Dataset loaded successfully")
        logger.info(f"Total records: {len(df)}")
        logger.info(f"Columns: {list(df.columns)}")
        logger.info(f"\nSample records (first 5):")
        logger.info(f"\n{df.head()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to load dataset '{dataset_name}': {str(e)}")
        raise Exception(f"Dataset loading failed: {str(e)}")


def validate_dataset_structure(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validate that the dataset contains all required columns.
    
    Args:
        df: DataFrame to validate.
        required_columns: List of column names that must be present.
        
    Returns:
        True if all required columns are present.
        
    Raises:
        ValueError: If required columns are missing.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    return True

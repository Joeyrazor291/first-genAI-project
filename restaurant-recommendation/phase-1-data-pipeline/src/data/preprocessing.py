"""Data cleaning and normalization module."""

import logging
import pandas as pd
import re
from typing import List

from src.config import CRITICAL_FIELDS, MIN_RATING, MAX_RATING, MIN_PRICE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def to_snake_case(name: str) -> str:
    """
    Convert a string to snake_case.
    
    Args:
        name: String to convert.
        
    Returns:
        snake_case version of the string.
    """
    # Remove parentheses and their contents
    name = re.sub(r'\([^)]*\)', '', name)
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[\s\-]+', '_', name)
    # Insert underscore before uppercase letters and convert to lowercase
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    # Remove trailing underscores
    name = name.strip('_')
    return name.lower()


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to snake_case.
    
    Args:
        df: DataFrame with original column names.
        
    Returns:
        DataFrame with normalized column names.
    """
    df.columns = [to_snake_case(col) for col in df.columns]
    return df


def clean_restaurant_data(df: pd.DataFrame, critical_fields: List[str] = None) -> pd.DataFrame:
    """
    Clean and normalize restaurant data.
    
    Steps:
    1. Normalize column names to snake_case
    2. Map Hugging Face dataset columns to expected format
    3. Drop rows with null critical fields
    4. Standardize data types
    5. Flag and remove anomalous data
    6. Remove duplicates
    
    Args:
        df: Raw restaurant DataFrame.
        critical_fields: List of fields that must not be null.
        
    Returns:
        Cleaned DataFrame.
    """
    critical_fields = critical_fields or CRITICAL_FIELDS
    
    logger.info(f"Starting data cleaning. Initial record count: {len(df)}")
    
    # Step 1: Normalize column names
    df = normalize_column_names(df)
    logger.info(f"Column names normalized: {list(df.columns)}")
    
    # Step 2: Map Hugging Face dataset columns to expected format
    column_mapping = {
        'cuisines': 'cuisine',
        'rate': 'rating',
        'approx_cost': 'price',  # After snake_case, "approx_cost(for two people)" becomes "approx_cost"
        'listed_in_city': 'city'
    }
    
    # Rename columns if they exist
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
            logger.info(f"Mapped column '{old_col}' to '{new_col}'")
    
    # Extract numeric rating from string format (e.g., "4.1/5" -> 4.1)
    if 'rating' in df.columns:
        df['rating'] = df['rating'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    
    # Extract numeric price from string format (e.g., "800" or "800,000")
    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).str.replace(',', '')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        # Divide by 2 to get price per person (dataset has price for two)
        df['price'] = df['price'] / 2
    
    logger.info(f"Columns after mapping: {list(df.columns)}")
    
    # Step 3: Drop rows with null critical fields
    initial_count = len(df)
    df = df.dropna(subset=critical_fields)
    dropped_null = initial_count - len(df)
    if dropped_null > 0:
        logger.info(f"Dropped {dropped_null} rows with null critical fields")
    
    # Step 4: Standardize data types
    
    # Convert cuisine and location to lowercase stripped strings
    if 'cuisine' in df.columns:
        # Take only the first cuisine if multiple are listed
        df['cuisine'] = df['cuisine'].astype(str).str.split(',').str[0].str.strip().str.lower()
    
    if 'location' in df.columns:
        df['location'] = df['location'].astype(str).str.strip().str.lower()
    
    if 'name' in df.columns:
        df['name'] = df['name'].astype(str).str.strip()
    
    # Add address if available
    if 'address' in df.columns:
        df['address'] = df['address'].astype(str).str.strip()
    
    # Step 5: Flag and remove anomalous data
    anomalies_count = 0
    
    # Check for out-of-range ratings
    if 'rating' in df.columns:
        invalid_ratings = (df['rating'] < MIN_RATING) | (df['rating'] > MAX_RATING) | df['rating'].isna()
        if invalid_ratings.any():
            anomalies_count += invalid_ratings.sum()
            logger.warning(f"Found {invalid_ratings.sum()} records with invalid ratings (not in {MIN_RATING}-{MAX_RATING} range)")
            df = df[~invalid_ratings]
    
    # Check for negative prices
    if 'price' in df.columns:
        invalid_prices = (df['price'] < MIN_PRICE) | df['price'].isna()
        if invalid_prices.any():
            anomalies_count += invalid_prices.sum()
            logger.warning(f"Found {invalid_prices.sum()} records with invalid prices (negative or null)")
            df = df[~invalid_prices]
    
    if anomalies_count > 0:
        logger.info(f"Removed {anomalies_count} anomalous records")
    
    # Step 6: Remove duplicates based on name and location
    initial_count = len(df)
    df = df.drop_duplicates(subset=['name', 'location'], keep='first')
    dropped_duplicates = initial_count - len(df)
    if dropped_duplicates > 0:
        logger.info(f"Removed {dropped_duplicates} duplicate records")
    
    # Step 7: Keep only required columns for storage
    required_cols = ['name', 'cuisine', 'location', 'rating', 'price']
    optional_cols = ['address']
    
    # Keep only columns that exist
    cols_to_keep = [col for col in required_cols + optional_cols if col in df.columns]
    df = df[cols_to_keep]
    
    logger.info(f"Data cleaning complete. Final record count: {len(df)}")
    logger.info(f"Final columns: {list(df.columns)}")
    
    return df


def get_cleaning_summary(original_count: int, cleaned_count: int) -> dict:
    """
    Generate a summary of the cleaning process.
    
    Args:
        original_count: Number of records before cleaning.
        cleaned_count: Number of records after cleaning.
        
    Returns:
        Dictionary with cleaning statistics.
    """
    return {
        'original_count': original_count,
        'cleaned_count': cleaned_count,
        'removed_count': original_count - cleaned_count,
        'retention_rate': f"{(cleaned_count / original_count * 100):.2f}%" if original_count > 0 else "0%"
    }

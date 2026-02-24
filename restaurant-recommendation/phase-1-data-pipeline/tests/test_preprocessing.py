"""Tests for data preprocessing module."""

import pytest
import pandas as pd
from src.data.preprocessing import (
    clean_restaurant_data,
    normalize_column_names,
    to_snake_case,
    get_cleaning_summary
)


class TestColumnNormalization:
    """Test cases for column name normalization."""
    
    def test_to_snake_case_conversion(self):
        """Test snake_case conversion for various input formats."""
        assert to_snake_case('CamelCase') == 'camel_case'
        assert to_snake_case('snake_case') == 'snake_case'
        assert to_snake_case('Space Separated') == 'space_separated'
        assert to_snake_case('kebab-case') == 'kebab_case'
        assert to_snake_case('Mixed-Format Name') == 'mixed_format_name'
    
    def test_normalize_column_names(self, sample_raw_dataframe):
        """Test that column names are normalized to snake_case."""
        df = normalize_column_names(sample_raw_dataframe.copy())
        
        expected_columns = ['name', 'cuisine', 'location', 'rating', 'price']
        assert list(df.columns) == expected_columns


class TestDataCleaning:
    """Test cases for data cleaning functionality."""
    
    def test_rows_with_null_critical_fields_removed(self, sample_raw_dataframe):
        """Test that rows with null critical fields are removed."""
        critical_fields = ['name', 'cuisine', 'location', 'rating', 'price']
        
        df = clean_restaurant_data(sample_raw_dataframe.copy(), critical_fields)
        
        # Check that no null values exist in critical fields
        for field in critical_fields:
            assert df[field].notna().all()
    
    def test_column_names_in_snake_case_after_normalization(self, sample_raw_dataframe):
        """Test that column names are in snake_case after cleaning."""
        df = clean_restaurant_data(sample_raw_dataframe.copy())
        
        expected_columns = ['name', 'cuisine', 'location', 'rating', 'price']
        assert list(df.columns) == expected_columns
    
    def test_ratings_are_floats_within_range(self, sample_raw_dataframe):
        """Test that ratings are floats within 0.0-5.0 range."""
        df = clean_restaurant_data(sample_raw_dataframe.copy())
        
        assert df['rating'].dtype in [float, 'float64']
        assert (df['rating'] >= 0.0).all()
        assert (df['rating'] <= 5.0).all()
    
    def test_price_values_are_numeric_and_non_negative(self, sample_raw_dataframe):
        """Test that price values are numeric and non-negative."""
        df = clean_restaurant_data(sample_raw_dataframe.copy())
        
        assert pd.api.types.is_numeric_dtype(df['price'])
        assert (df['price'] >= 0).all()
    
    def test_cuisine_and_location_lowercase_and_stripped(self, sample_raw_dataframe):
        """Test that cuisine and location values are lowercase and stripped."""
        df = clean_restaurant_data(sample_raw_dataframe.copy())
        
        # Check cuisine
        for value in df['cuisine']:
            assert value == value.lower()
            assert value == value.strip()
        
        # Check location
        for value in df['location']:
            assert value == value.lower()
            assert value == value.strip()
    
    def test_anomalous_rows_flagged_and_excluded(self, sample_raw_dataframe):
        """Test that anomalous rows are flagged and excluded."""
        initial_count = len(sample_raw_dataframe)
        df = clean_restaurant_data(sample_raw_dataframe.copy())
        
        # Should have removed rows with:
        # - null values in critical fields
        # - rating out of range (6.0)
        # - negative price (-10.00)
        # - duplicates
        assert len(df) < initial_count
        
        # Verify no anomalies remain
        assert (df['rating'] >= 0.0).all() and (df['rating'] <= 5.0).all()
        assert (df['price'] >= 0).all()
    
    def test_no_duplicate_restaurant_entries(self, sample_raw_dataframe):
        """Test that duplicate restaurant entries are removed."""
        df = clean_restaurant_data(sample_raw_dataframe.copy())
        
        # Check for duplicates based on name and location
        duplicates = df.duplicated(subset=['name', 'location'], keep=False)
        assert not duplicates.any()


class TestCleaningSummary:
    """Test cases for cleaning summary generation."""
    
    def test_cleaning_summary_calculation(self):
        """Test that cleaning summary calculates correct statistics."""
        summary = get_cleaning_summary(original_count=100, cleaned_count=85)
        
        assert summary['original_count'] == 100
        assert summary['cleaned_count'] == 85
        assert summary['removed_count'] == 15
        assert summary['retention_rate'] == "85.00%"
    
    def test_cleaning_summary_with_zero_original(self):
        """Test cleaning summary handles zero original count."""
        summary = get_cleaning_summary(original_count=0, cleaned_count=0)
        
        assert summary['retention_rate'] == "0%"

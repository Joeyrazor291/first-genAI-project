"""Tests for data ingestion module."""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data.ingestion import load_restaurant_dataset, validate_dataset_structure


class TestDatasetLoading:
    """Test cases for dataset loading functionality."""
    
    @patch('src.data.ingestion.load_dataset')
    def test_dataset_loads_without_errors(self, mock_load_dataset, sample_raw_dataframe):
        """Test that dataset loads successfully without errors."""
        # Mock the Hugging Face dataset
        mock_dataset = MagicMock()
        mock_dataset.__getitem__.return_value.to_pandas.return_value = sample_raw_dataframe
        mock_dataset.keys.return_value = ['train']
        mock_dataset.__contains__.return_value = True
        mock_load_dataset.return_value = mock_dataset
        
        # Load dataset
        df = load_restaurant_dataset('test/dataset')
        
        # Assertions
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        mock_load_dataset.assert_called_once()
    
    @patch('src.data.ingestion.load_dataset')
    def test_loaded_data_is_non_empty(self, mock_load_dataset, sample_raw_dataframe):
        """Test that loaded data is a non-empty DataFrame."""
        # Mock the dataset
        mock_dataset = MagicMock()
        mock_dataset.__getitem__.return_value.to_pandas.return_value = sample_raw_dataframe
        mock_dataset.keys.return_value = ['train']
        mock_dataset.__contains__.return_value = True
        mock_load_dataset.return_value = mock_dataset
        
        df = load_restaurant_dataset('test/dataset')
        
        assert len(df) > 0
        assert not df.empty
    
    @patch('src.data.ingestion.load_dataset')
    def test_all_expected_columns_present(self, mock_load_dataset, sample_raw_dataframe):
        """Test that all expected columns are present in loaded data."""
        # Mock the dataset
        mock_dataset = MagicMock()
        mock_dataset.__getitem__.return_value.to_pandas.return_value = sample_raw_dataframe
        mock_dataset.keys.return_value = ['train']
        mock_dataset.__contains__.return_value = True
        mock_load_dataset.return_value = mock_dataset
        
        df = load_restaurant_dataset('test/dataset')
        
        expected_columns = ['Name', 'Cuisine', 'Location', 'Rating', 'Price']
        for col in expected_columns:
            assert col in df.columns
    
    @patch('src.data.ingestion.load_dataset')
    def test_handles_invalid_dataset_gracefully(self, mock_load_dataset):
        """Test that invalid dataset path/name raises appropriate exception."""
        # Mock a failed dataset load
        mock_load_dataset.side_effect = Exception("Dataset not found")
        
        with pytest.raises(Exception) as exc_info:
            load_restaurant_dataset('invalid/dataset')
        
        assert "Dataset loading failed" in str(exc_info.value)


class TestDatasetValidation:
    """Test cases for dataset structure validation."""
    
    def test_validate_dataset_with_all_columns(self, sample_raw_dataframe):
        """Test validation passes when all required columns are present."""
        required_columns = ['Name', 'Cuisine', 'Location']
        
        result = validate_dataset_structure(sample_raw_dataframe, required_columns)
        
        assert result is True
    
    def test_validate_dataset_with_missing_columns(self, sample_raw_dataframe):
        """Test validation fails when required columns are missing."""
        required_columns = ['Name', 'Cuisine', 'NonExistentColumn']
        
        with pytest.raises(ValueError) as exc_info:
            validate_dataset_structure(sample_raw_dataframe, required_columns)
        
        assert "Missing required columns" in str(exc_info.value)
        assert "NonExistentColumn" in str(exc_info.value)

"""Tests for data store module."""

import pytest
import pandas as pd
from pathlib import Path
from src.data.store import RestaurantStore


class TestDatabaseCreation:
    """Test cases for database creation and initialization."""
    
    def test_sqlite_db_created_successfully(self, temp_db_path):
        """Test that SQLite database is created at configured path."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        
        assert temp_db_path.exists()
        store.close()
    
    def test_restaurants_table_exists(self, temp_db_path, sample_cleaned_dataframe):
        """Test that restaurants table exists with correct schema."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        # Query to check table existence
        result = store.get_all()
        assert result is not None
        assert len(result) > 0
        
        store.close()


class TestDataInsertion:
    """Test cases for data insertion into database."""
    
    def test_records_inserted_match_dataframe_count(self, temp_db_path, sample_cleaned_dataframe):
        """Test that inserted records match DataFrame row count."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        stats = store.get_stats()
        assert stats['total_restaurants'] == len(sample_cleaned_dataframe)
        
        store.close()
    
    def test_reinserting_data_does_not_create_duplicates(self, temp_db_path, sample_cleaned_dataframe):
        """Test that reinserting data is idempotent (replaces instead of duplicating)."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        
        # Insert data twice with replace=True
        store.store_restaurants(sample_cleaned_dataframe, replace=True)
        store.store_restaurants(sample_cleaned_dataframe, replace=True)
        
        stats = store.get_stats()
        # Should still have the same count, not doubled
        assert stats['total_restaurants'] == len(sample_cleaned_dataframe)
        
        store.close()


class TestDataQuerying:
    """Test cases for querying restaurant data."""
    
    def test_filter_restaurants_returns_correct_results(self, temp_db_path, sample_cleaned_dataframe):
        """Test that filter_restaurants returns correct results for valid inputs."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        # Filter by cuisine
        results = store.filter_restaurants(cuisine='italian')
        assert len(results) > 0
        assert all(r['cuisine'] == 'italian' for r in results)
        
        # Filter by minimum rating
        results = store.filter_restaurants(min_rating=4.0)
        assert all(r['rating'] >= 4.0 for r in results)
        
        # Filter by maximum price
        results = store.filter_restaurants(max_price=20.0)
        assert all(r['price'] <= 20.0 for r in results)
        
        # Combined filters
        results = store.filter_restaurants(cuisine='italian', min_rating=4.0)
        assert all(r['cuisine'] == 'italian' and r['rating'] >= 4.0 for r in results)
        
        store.close()
    
    def test_filter_restaurants_returns_empty_list_for_no_matches(self, temp_db_path, sample_cleaned_dataframe):
        """Test that filter_restaurants returns empty list for no-match queries."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        # Query for non-existent cuisine
        results = store.filter_restaurants(cuisine='nonexistent')
        assert results == []
        assert isinstance(results, list)
        
        # Query for impossible rating
        results = store.filter_restaurants(min_rating=10.0)
        assert results == []
        
        store.close()
    
    def test_get_all_returns_all_records(self, temp_db_path, sample_cleaned_dataframe):
        """Test that get_all returns all records as list of dicts."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        results = store.get_all()
        
        assert isinstance(results, list)
        assert len(results) == len(sample_cleaned_dataframe)
        assert all(isinstance(r, dict) for r in results)
        
        # Check that all expected keys are present
        expected_keys = ['name', 'cuisine', 'location', 'rating', 'price']
        for result in results:
            for key in expected_keys:
                assert key in result
        
        store.close()
    
    def test_get_stats_returns_correct_counts(self, temp_db_path, sample_cleaned_dataframe):
        """Test that get_stats returns correct statistics."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        stats = store.get_stats()
        
        assert 'total_restaurants' in stats
        assert 'unique_cuisines' in stats
        assert 'unique_locations' in stats
        
        assert stats['total_restaurants'] == len(sample_cleaned_dataframe)
        assert stats['unique_cuisines'] == sample_cleaned_dataframe['cuisine'].nunique()
        assert stats['unique_locations'] == sample_cleaned_dataframe['location'].nunique()
        
        store.close()


class TestEdgeCases:
    """Test cases for edge cases and error handling."""
    
    def test_store_empty_dataframe(self, temp_db_path):
        """Test storing an empty DataFrame."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        
        empty_df = pd.DataFrame(columns=['name', 'cuisine', 'location', 'rating', 'price'])
        store.store_restaurants(empty_df)
        
        stats = store.get_stats()
        assert stats['total_restaurants'] == 0
        
        store.close()
    
    def test_filter_with_case_insensitive_search(self, temp_db_path, sample_cleaned_dataframe):
        """Test that filtering is case-insensitive."""
        store = RestaurantStore(db_path=temp_db_path)
        store.create_tables()
        store.store_restaurants(sample_cleaned_dataframe)
        
        # Search with different cases
        results_lower = store.filter_restaurants(cuisine='italian')
        results_upper = store.filter_restaurants(cuisine='ITALIAN')
        results_mixed = store.filter_restaurants(cuisine='Italian')
        
        assert len(results_lower) == len(results_upper) == len(results_mixed)
        
        store.close()

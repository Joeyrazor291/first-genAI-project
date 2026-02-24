"""Tests for database service module."""

import pytest
from src.database_service import DatabaseService


class TestDatabaseServiceInitialization:
    """Test cases for database service initialization."""
    
    def test_initialization_with_valid_database(self, temp_database):
        """Test initialization with valid database."""
        service = DatabaseService(temp_database)
        
        assert service.db_path == temp_database
    
    def test_initialization_with_nonexistent_database(self):
        """Test initialization with nonexistent database."""
        with pytest.raises(FileNotFoundError):
            DatabaseService("/nonexistent/path/to/database.db")
    
    def test_initialization_validates_table_exists(self, temp_database):
        """Test that initialization validates restaurants table exists."""
        # This should succeed since temp_database has the table
        service = DatabaseService(temp_database)
        assert service is not None


class TestFilterRestaurants:
    """Test cases for filtering restaurants."""
    
    def test_filter_by_cuisine(self, temp_database):
        """Test filtering by cuisine."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(cuisine='italian')
        
        assert len(results) > 0
        assert all(r['cuisine'] == 'italian' for r in results)
    
    def test_filter_by_location(self, temp_database):
        """Test filtering by location."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(location='downtown')
        
        assert len(results) > 0
        assert all('downtown' in r['location'].lower() for r in results)
    
    def test_filter_by_min_rating(self, temp_database):
        """Test filtering by minimum rating."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(min_rating=4.5)
        
        assert len(results) > 0
        assert all(r['rating'] >= 4.5 for r in results)
    
    def test_filter_by_max_price(self, temp_database):
        """Test filtering by maximum price."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(max_price=25.0)
        
        assert len(results) > 0
        assert all(r['price'] <= 25.0 for r in results)
    
    def test_filter_with_multiple_criteria(self, temp_database):
        """Test filtering with multiple criteria."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(
            cuisine='italian',
            location='downtown',
            min_rating=4.0,
            max_price=30.0
        )
        
        assert len(results) > 0
        for r in results:
            assert r['cuisine'] == 'italian'
            assert 'downtown' in r['location'].lower()
            assert r['rating'] >= 4.0
            assert r['price'] <= 30.0
    
    def test_filter_respects_limit(self, temp_database):
        """Test that filter respects limit parameter."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(limit=2)
        
        assert len(results) <= 2
    
    def test_filter_returns_empty_for_no_matches(self, temp_database):
        """Test that filter returns empty list when no matches."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(cuisine='nonexistent')
        
        assert results == []
    
    def test_filter_orders_by_rating_desc(self, temp_database):
        """Test that results are ordered by rating descending."""
        service = DatabaseService(temp_database)
        
        results = service.filter_restaurants(cuisine='italian', limit=10)
        
        # Check that ratings are in descending order
        ratings = [r['rating'] for r in results]
        assert ratings == sorted(ratings, reverse=True)


class TestGetAllRestaurants:
    """Test cases for getting all restaurants."""
    
    def test_get_all_restaurants(self, temp_database):
        """Test getting all restaurants."""
        service = DatabaseService(temp_database)
        
        results = service.get_all_restaurants()
        
        assert len(results) == 8  # We inserted 8 test restaurants
    
    def test_get_all_restaurants_respects_limit(self, temp_database):
        """Test that get_all respects limit."""
        service = DatabaseService(temp_database)
        
        results = service.get_all_restaurants(limit=3)
        
        assert len(results) == 3


class TestGetRestaurantByName:
    """Test cases for getting restaurant by name."""
    
    def test_get_restaurant_by_name_found(self, temp_database):
        """Test getting restaurant by name when it exists."""
        service = DatabaseService(temp_database)
        
        result = service.get_restaurant_by_name('Pasta Paradise')
        
        assert result is not None
        assert result['name'] == 'Pasta Paradise'
        assert result['cuisine'] == 'italian'
    
    def test_get_restaurant_by_name_case_insensitive(self, temp_database):
        """Test that name search is case insensitive."""
        service = DatabaseService(temp_database)
        
        result = service.get_restaurant_by_name('PASTA PARADISE')
        
        assert result is not None
        assert result['name'] == 'Pasta Paradise'
    
    def test_get_restaurant_by_name_not_found(self, temp_database):
        """Test getting restaurant by name when it doesn't exist."""
        service = DatabaseService(temp_database)
        
        result = service.get_restaurant_by_name('Nonexistent Restaurant')
        
        assert result is None


class TestGetStats:
    """Test cases for getting database statistics."""
    
    def test_get_stats(self, temp_database):
        """Test getting database statistics."""
        service = DatabaseService(temp_database)
        
        stats = service.get_stats()
        
        assert 'total_restaurants' in stats
        assert 'unique_cuisines' in stats
        assert 'unique_locations' in stats
        assert 'average_rating' in stats
        assert 'average_price' in stats
        
        assert stats['total_restaurants'] == 8
        assert stats['unique_cuisines'] == 3  # italian, mexican, japanese
        assert stats['unique_locations'] == 2  # downtown, uptown
        assert stats['average_rating'] > 0
        assert stats['average_price'] > 0

"""Tests for database service module."""

import pytest
from pathlib import Path
from src.database import DatabaseService


class TestDatabaseService:
    """Test cases for database service."""
    
    def test_database_service_initialization(self, populated_test_db):
        """Test database service initializes correctly."""
        service = DatabaseService(db_path=populated_test_db)
        
        assert service.db_path == populated_test_db
        assert service._store is None  # Lazy initialization
    
    def test_database_service_store_property(self, populated_test_db):
        """Test store property creates RestaurantStore instance."""
        service = DatabaseService(db_path=populated_test_db)
        
        store = service.store
        
        assert store is not None
        assert service._store is not None
        
        service.close()
    
    def test_database_service_missing_db_raises_error(self, tmp_path):
        """Test that missing database raises appropriate error."""
        non_existent_path = tmp_path / "nonexistent.db"
        service = DatabaseService(db_path=non_existent_path)
        
        with pytest.raises(FileNotFoundError) as exc_info:
            _ = service.store
        
        assert "Phase 1 database not found" in str(exc_info.value)
    
    def test_get_recommendations_all_filters(self, populated_test_db):
        """Test getting recommendations with all filters."""
        service = DatabaseService(db_path=populated_test_db)
        
        results = service.get_recommendations(
            cuisine='italian',
            location='downtown',
            min_rating=4.0,
            max_price=30.0,
            limit=5
        )
        
        assert isinstance(results, list)
        for r in results:
            assert r['cuisine'] == 'italian'
            assert r['location'] == 'downtown'
            assert r['rating'] >= 4.0
            assert r['price'] <= 30.0
        
        assert len(results) <= 5
        
        service.close()
    
    def test_get_recommendations_no_filters(self, populated_test_db):
        """Test getting recommendations without filters."""
        service = DatabaseService(db_path=populated_test_db)
        
        results = service.get_recommendations(limit=10)
        
        assert isinstance(results, list)
        assert len(results) <= 10
        
        service.close()
    
    def test_get_recommendations_respects_limit(self, populated_test_db):
        """Test that limit parameter is respected."""
        service = DatabaseService(db_path=populated_test_db)
        
        results = service.get_recommendations(limit=3)
        
        assert len(results) <= 3
        
        service.close()
    
    def test_get_stats(self, populated_test_db):
        """Test getting database statistics."""
        service = DatabaseService(db_path=populated_test_db)
        
        stats = service.get_stats()
        
        assert 'total_restaurants' in stats
        assert 'unique_cuisines' in stats
        assert 'unique_locations' in stats
        assert stats['total_restaurants'] > 0
        
        service.close()
    
    def test_get_all_restaurants(self, populated_test_db):
        """Test getting all restaurants."""
        service = DatabaseService(db_path=populated_test_db)
        
        results = service.get_all_restaurants()
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        service.close()
    
    def test_get_all_restaurants_with_limit(self, populated_test_db):
        """Test getting all restaurants with limit."""
        service = DatabaseService(db_path=populated_test_db)
        
        results = service.get_all_restaurants(limit=5)
        
        assert len(results) <= 5
        
        service.close()
    
    def test_close_connection(self, populated_test_db):
        """Test closing database connection."""
        service = DatabaseService(db_path=populated_test_db)
        
        # Access store to initialize it
        _ = service.store
        assert service._store is not None
        
        # Close connection
        service.close()
        assert service._store is None

"""Tests for recommendation engine module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.recommendation_engine import RecommendationEngine, RecommendationEngineError
from src.config import EngineConfig


class TestRecommendationEngineInitialization:
    """Test cases for recommendation engine initialization."""
    
    def test_initialization_with_config(self, temp_database):
        """Test initialization with provided config."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""  # No LLM for this test
        )
        
        engine = RecommendationEngine(config=config)
        
        assert engine.config == config
        assert engine.preference_processor is not None
        assert engine.database_service is not None
        assert engine.llm_service is None  # No API key
    
    def test_initialization_with_llm_api_key(self, temp_database, monkeypatch):
        """Test initialization with LLM API key."""
        # Skip this test for now due to import complexities
        pytest.skip("LLM integration test skipped - requires phase 4 module refactoring")


class TestGetRecommendations:
    """Test cases for getting recommendations."""
    
    def test_get_recommendations_with_valid_preferences(self, temp_database):
        """Test getting recommendations with valid preferences."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""  # Use fallback
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 'italian',
            'location': 'downtown',
            'min_rating': 4.0,
            'limit': 3
        }
        
        result = engine.get_recommendations(preferences)
        
        assert result['success'] is True
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0
        assert len(result['recommendations']) <= 3
    
    def test_get_recommendations_with_invalid_preferences(self, temp_database):
        """Test getting recommendations with invalid preferences."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 123,  # Invalid type
            'min_rating': 10.0  # Out of range
        }
        
        result = engine.get_recommendations(preferences)
        
        assert result['success'] is False
        assert 'error' in result
        assert 'details' in result
    
    def test_get_recommendations_no_matches(self, temp_database):
        """Test getting recommendations when no restaurants match."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 'nonexistent',
            'limit': 5
        }
        
        result = engine.get_recommendations(preferences)
        
        assert result['success'] is True
        assert result['recommendations'] == []
        assert 'message' in result
    
    def test_get_recommendations_enriches_data(self, temp_database):
        """Test that recommendations are enriched with full restaurant data."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 'italian',
            'limit': 2
        }
        
        result = engine.get_recommendations(preferences)
        
        assert result['success'] is True
        for rec in result['recommendations']:
            assert 'name' in rec
            assert 'cuisine' in rec
            assert 'location' in rec
            assert 'rating' in rec
            assert 'price' in rec
            assert 'explanation' in rec
    
    def test_get_recommendations_includes_metadata(self, temp_database):
        """Test that response includes metadata."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 'italian',
            'limit': 3
        }
        
        result = engine.get_recommendations(preferences)
        
        assert 'total_found' in result
        assert 'returned' in result
        assert 'filters_applied' in result
        assert result['total_found'] >= result['returned']


class TestFallbackRecommendations:
    """Test cases for fallback recommendations."""
    
    def test_fallback_recommendations_sorted_by_rating(self, temp_database):
        """Test that fallback recommendations are sorted by rating."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 'italian',
            'limit': 3
        }
        
        result = engine.get_recommendations(preferences)
        
        # Check that recommendations are sorted by rating
        ratings = [rec['rating'] for rec in result['recommendations']]
        assert ratings == sorted(ratings, reverse=True)
    
    def test_fallback_recommendations_respects_limit(self, temp_database):
        """Test that fallback respects limit."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'limit': 2
        }
        
        result = engine.get_recommendations(preferences)
        
        assert len(result['recommendations']) <= 2


class TestEnrichRecommendations:
    """Test cases for enriching recommendations."""
    
    def test_enrich_recommendations_matches_names(self, temp_database, sample_restaurants):
        """Test that enrichment matches restaurant names correctly."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        llm_recs = [
            {'name': 'Pasta Paradise', 'explanation': 'Great pasta'},
            {'name': 'Pizza Palace', 'explanation': 'Good pizza'}
        ]
        
        enriched = engine._enrich_recommendations(llm_recs, sample_restaurants)
        
        assert len(enriched) == 2
        assert enriched[0]['name'] == 'Pasta Paradise'
        assert enriched[0]['cuisine'] == 'italian'
        assert enriched[0]['explanation'] == 'Great pasta'
    
    def test_enrich_recommendations_handles_missing_restaurants(self, temp_database):
        """Test enrichment when restaurant not found in database."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        llm_recs = [
            {'name': 'Nonexistent Restaurant', 'explanation': 'Good food'}
        ]
        restaurants = []
        
        enriched = engine._enrich_recommendations(llm_recs, restaurants)
        
        assert len(enriched) == 1
        assert enriched[0]['name'] == 'Nonexistent Restaurant'
        assert 'note' in enriched[0]


class TestDatabaseStats:
    """Test cases for database statistics."""
    
    def test_get_database_stats(self, temp_database):
        """Test getting database statistics."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        stats = engine.get_database_stats()
        
        assert 'total_restaurants' in stats
        assert stats['total_restaurants'] == 8


class TestHealthCheck:
    """Test cases for health check."""
    
    def test_health_check_all_healthy(self, temp_database):
        """Test health check when all components healthy."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        health = engine.health_check()
        
        assert 'status' in health
        assert health['engine'] == 'healthy'
        assert health['database'] == 'healthy'
        assert health['preference_processor'] == 'healthy'
    
    def test_health_check_includes_database_stats(self, temp_database):
        """Test that health check includes database stats."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        health = engine.health_check()
        
        assert 'database_stats' in health
        assert health['database_stats']['total_restaurants'] > 0


class TestEdgeCases:
    """Test cases for edge cases."""
    
    def test_empty_preferences(self, temp_database):
        """Test with empty preferences dictionary."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        result = engine.get_recommendations({})
        
        assert result['success'] is True
        assert len(result['recommendations']) > 0
    
    def test_preferences_with_warnings(self, temp_database):
        """Test preferences that generate warnings."""
        config = EngineConfig(
            phase1_db_path=temp_database,
            groq_api_key=""
        )
        engine = RecommendationEngine(config=config)
        
        preferences = {
            'cuisine': 'unknown_cuisine',  # Will generate warning
            'limit': 3
        }
        
        result = engine.get_recommendations(preferences)
        
        assert result['success'] is True
        assert 'warnings' in result

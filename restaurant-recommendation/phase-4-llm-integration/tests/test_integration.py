"""Integration tests for Phase 4 LLM Integration (requires API key)."""

import pytest
import os
from src.llm_service import LLMService, LLMServiceError
from src.config import LLMConfig
from src.prompt_builder import PromptBuilder


# Skip all tests if no API key is available
pytestmark = pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY not set - integration tests require API key"
)


@pytest.mark.integration
class TestLLMServiceIntegration:
    """Integration tests for LLM service with real API calls."""
    
    def test_service_initialization_from_env(self):
        """Test service initializes correctly from environment."""
        service = LLMService()
        
        assert service.config is not None
        assert service.config.api_key is not None
        assert service.client is not None
        assert service.prompt_builder is not None
    
    def test_health_check_with_real_api(self):
        """Test health check with real API."""
        service = LLMService()
        
        health = service.health_check()
        
        assert health['status'] == 'healthy'
        assert health['api_accessible'] is True
        assert 'model' in health
        assert health['model'] == service.config.model
    
    def test_generate_recommendations_basic(self, sample_preferences, sample_restaurants):
        """Test basic recommendation generation with real API."""
        service = LLMService()
        
        recommendations = service.generate_recommendations(
            preferences=sample_preferences,
            restaurants=sample_restaurants,
            limit=3
        )
        
        # Validate response structure
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert len(recommendations) <= 3
        
        # Validate each recommendation
        for rec in recommendations:
            assert isinstance(rec, dict)
            assert 'name' in rec
            assert 'explanation' in rec
            assert isinstance(rec['name'], str)
            assert isinstance(rec['explanation'], str)
            assert len(rec['name']) > 0
            assert len(rec['explanation']) > 0
    
    def test_generate_recommendations_with_minimal_preferences(
        self, minimal_preferences, sample_restaurants
    ):
        """Test recommendation generation with minimal preferences."""
        service = LLMService()
        
        recommendations = service.generate_recommendations(
            preferences=minimal_preferences,
            restaurants=sample_restaurants,
            limit=5
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
    
    def test_generate_recommendations_respects_limit(
        self, sample_preferences, sample_restaurants
    ):
        """Test that recommendation limit is respected."""
        service = LLMService()
        
        # Test with limit of 2
        recommendations = service.generate_recommendations(
            preferences=sample_preferences,
            restaurants=sample_restaurants,
            limit=2
        )
        
        assert len(recommendations) <= 2
    
    def test_generate_recommendations_with_single_restaurant(
        self, sample_preferences
    ):
        """Test recommendation generation with single restaurant."""
        service = LLMService()
        
        single_restaurant = [{
            'name': 'Solo Restaurant',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.5,
            'price': 25.0
        }]
        
        recommendations = service.generate_recommendations(
            preferences=sample_preferences,
            restaurants=single_restaurant,
            limit=1
        )
        
        assert len(recommendations) == 1
        assert recommendations[0]['name'] == 'Solo Restaurant'
    
    def test_generate_recommendations_with_different_cuisines(self):
        """Test recommendations with various cuisine types."""
        service = LLMService()
        
        preferences = {
            'cuisine': 'mexican',
            'min_rating': 4.0
        }
        
        restaurants = [
            {
                'name': 'Taco Heaven',
                'cuisine': 'mexican',
                'location': 'downtown',
                'rating': 4.6,
                'price': 15.0
            },
            {
                'name': 'Burrito Palace',
                'cuisine': 'mexican',
                'location': 'uptown',
                'rating': 4.4,
                'price': 12.0
            }
        ]
        
        recommendations = service.generate_recommendations(
            preferences=preferences,
            restaurants=restaurants,
            limit=2
        )
        
        assert len(recommendations) > 0
        # Verify recommendations are from the provided list
        rec_names = [r['name'] for r in recommendations]
        assert all(name in ['Taco Heaven', 'Burrito Palace'] for name in rec_names)
    
    def test_generate_recommendations_with_price_preference(self):
        """Test recommendations considering price preferences."""
        service = LLMService()
        
        preferences = {
            'cuisine': 'italian',
            'max_price': 20.0
        }
        
        restaurants = [
            {
                'name': 'Budget Italian',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.2,
                'price': 15.0
            },
            {
                'name': 'Expensive Italian',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.8,
                'price': 50.0
            }
        ]
        
        recommendations = service.generate_recommendations(
            preferences=preferences,
            restaurants=restaurants,
            limit=2
        )
        
        assert len(recommendations) > 0
    
    def test_generate_recommendations_with_rating_preference(self):
        """Test recommendations considering rating preferences."""
        service = LLMService()
        
        preferences = {
            'cuisine': 'italian',
            'min_rating': 4.5
        }
        
        restaurants = [
            {
                'name': 'High Rated',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.8,
                'price': 30.0
            },
            {
                'name': 'Low Rated',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 3.5,
                'price': 20.0
            }
        ]
        
        recommendations = service.generate_recommendations(
            preferences=preferences,
            restaurants=restaurants,
            limit=2
        )
        
        assert len(recommendations) > 0


@pytest.mark.integration
class TestPromptBuilderIntegration:
    """Integration tests for prompt builder."""
    
    def test_build_prompt_produces_valid_structure(
        self, sample_preferences, sample_restaurants
    ):
        """Test that built prompts have valid structure."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            preferences=sample_preferences,
            restaurants=sample_restaurants,
            limit=5
        )
        
        # Verify prompt contains key sections
        assert 'User Preferences:' in prompt
        assert 'Available Restaurants:' in prompt
        assert 'Task:' in prompt
        assert 'JSON' in prompt
        
        # Verify preference details are included
        assert 'italian' in prompt.lower()
        assert 'downtown' in prompt.lower()
        
        # Verify restaurant details are included
        for restaurant in sample_restaurants:
            assert restaurant['name'] in prompt


@pytest.mark.integration
class TestConfigIntegration:
    """Integration tests for configuration."""
    
    def test_config_loads_from_env(self):
        """Test configuration loads correctly from environment."""
        config = LLMConfig.from_env()
        
        assert config.api_key is not None
        assert len(config.api_key) > 0
        assert config.model is not None
        assert config.temperature >= 0
        assert config.max_tokens > 0
    
    def test_config_validation_passes(self):
        """Test that environment config passes validation."""
        config = LLMConfig.from_env()
        
        # Should not raise any exception
        config.validate()


@pytest.mark.integration
class TestEndToEndFlow:
    """End-to-end integration tests."""
    
    def test_complete_recommendation_flow(self):
        """Test complete flow from preferences to recommendations."""
        # Step 1: Initialize service
        service = LLMService()
        
        # Step 2: Prepare data
        preferences = {
            'cuisine': 'italian',
            'location': 'downtown',
            'min_rating': 4.0,
            'max_price': 35.0,
            'limit': 3
        }
        
        restaurants = [
            {
                'name': 'Pasta Paradise',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.5,
                'price': 25.0
            },
            {
                'name': 'Pizza Palace',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.3,
                'price': 20.0
            },
            {
                'name': 'Trattoria Roma',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.7,
                'price': 35.0
            },
            {
                'name': 'Bella Italia',
                'cuisine': 'italian',
                'location': 'downtown',
                'rating': 4.2,
                'price': 28.0
            }
        ]
        
        # Step 3: Generate recommendations
        recommendations = service.generate_recommendations(
            preferences=preferences,
            restaurants=restaurants,
            limit=3
        )
        
        # Step 4: Validate results
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert len(recommendations) <= 3
        
        # Validate structure
        for rec in recommendations:
            assert 'name' in rec
            assert 'explanation' in rec
            assert len(rec['name']) > 0
            assert len(rec['explanation']) > 10  # Reasonable explanation length
            
            # Verify recommended restaurants are from the input list
            restaurant_names = [r['name'] for r in restaurants]
            assert rec['name'] in restaurant_names
    
    def test_fallback_flow_when_no_restaurants(self):
        """Test fallback when no restaurants match."""
        service = LLMService()
        
        preferences = {'cuisine': 'italian'}
        empty_restaurants = []
        
        # Should return empty list, not error
        recommendations = service.generate_recommendations(
            preferences=preferences,
            restaurants=empty_restaurants,
            limit=5
        )
        
        assert recommendations == []
    
    def test_multiple_consecutive_requests(self, sample_preferences, sample_restaurants):
        """Test multiple consecutive API requests."""
        service = LLMService()
        
        # Make 3 consecutive requests
        for i in range(3):
            recommendations = service.generate_recommendations(
                preferences=sample_preferences,
                restaurants=sample_restaurants,
                limit=2
            )
            
            assert len(recommendations) > 0
            assert len(recommendations) <= 2


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Integration tests for error handling."""
    
    def test_invalid_api_key_handling(self):
        """Test handling of invalid API key."""
        # Create config with invalid key
        config = LLMConfig(api_key="invalid_key_12345")
        service = LLMService(config=config)
        
        # Health check should fail
        health = service.health_check()
        assert health['status'] == 'unhealthy'
        assert health['api_accessible'] is False
    
    def test_fallback_recommendations_always_work(self, sample_restaurants):
        """Test that fallback recommendations work without API."""
        service = LLMService()
        
        fallback_recs = service.generate_fallback_recommendations(
            restaurants=sample_restaurants,
            limit=3
        )
        
        assert len(fallback_recs) == 3
        assert all('name' in rec for rec in fallback_recs)
        assert all('explanation' in rec for rec in fallback_recs)
        
        # Verify sorted by rating (highest first)
        ratings = [r.get('rating', 0) for r in sample_restaurants]
        max_rating = max(ratings)
        top_restaurant = [r for r in sample_restaurants if r.get('rating') == max_rating][0]
        assert fallback_recs[0]['name'] == top_restaurant['name']


@pytest.mark.integration
class TestPerformance:
    """Performance-related integration tests."""
    
    def test_response_time_reasonable(self, sample_preferences, sample_restaurants):
        """Test that response time is reasonable."""
        import time
        
        service = LLMService()
        
        start_time = time.time()
        recommendations = service.generate_recommendations(
            preferences=sample_preferences,
            restaurants=sample_restaurants,
            limit=3
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Should complete within 10 seconds (generous limit)
        assert response_time < 10.0
        
        # Log the actual time for monitoring
        print(f"\nResponse time: {response_time:.2f} seconds")
    
    def test_health_check_is_fast(self):
        """Test that health check is fast."""
        import time
        
        service = LLMService()
        
        start_time = time.time()
        health = service.health_check()
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Health check should be very fast (< 2 seconds)
        assert response_time < 2.0
        
        print(f"\nHealth check time: {response_time:.2f} seconds")


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v", "-m", "integration"])

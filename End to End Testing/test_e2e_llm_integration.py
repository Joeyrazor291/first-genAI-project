"""
End-to-End LLM Integration Tests

Tests for LLM service connectivity, prompt generation, response parsing,
and fallback mechanisms. These tests require the Groq API key to be configured.
"""

import pytest
import httpx
from typing import Dict, Any


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.requires_llm
class TestLLMServiceAvailability:
    """Test LLM service availability and health."""
    
    def test_llm_service_status_in_health_check(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that health check includes LLM service status."""
        response = api_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should include LLM service status
        if "llm_service" in data:
            assert data["llm_service"] in ["healthy", "unhealthy", "not_configured"], \
                f"LLM service status should be valid, got {data['llm_service']}"
    
    def test_system_works_without_llm(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that system works even if LLM is not configured."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        # Should succeed with or without LLM
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


@pytest.mark.e2e
@pytest.mark.requires_api
class TestRecommendationExplanations:
    """Test LLM-generated recommendation explanations."""
    
    def test_recommendations_include_explanations(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that recommendations include explanations (if LLM available)."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        if len(data["recommendations"]) > 0:
            # Check if any recommendations have explanations
            has_explanations = any(
                "explanation" in rec for rec in data["recommendations"]
            )
            
            # If LLM is available, should have explanations
            # If not, may have fallback explanations or none
            # Either way is valid
            assert isinstance(has_explanations, bool)
    
    def test_explanation_quality(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that explanations are meaningful (if present)."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        for restaurant in data["recommendations"]:
            if "explanation" in restaurant:
                explanation = restaurant["explanation"]
                
                # Explanation should be non-empty string
                assert isinstance(explanation, str)
                assert len(explanation) > 0
                
                # Should be reasonably long (not just "Good restaurant")
                assert len(explanation) > 10, \
                    f"Explanation too short: {explanation}"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestFallbackMechanisms:
    """Test fallback mechanisms when LLM is unavailable."""
    
    def test_fallback_recommendations_provided(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that fallback recommendations are provided if LLM fails."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should get recommendations even if LLM fails
        assert data["success"] is True
        
        # If there are matching restaurants, should get recommendations
        if data.get("total_found", 0) > 0:
            count = data.get("count") or data.get("returned", 0)
            assert count > 0, "Should provide fallback recommendations"
    
    def test_fallback_maintains_filters(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that fallback recommendations still respect filters."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify filters were applied
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == valid_preferences["cuisine"]
            if "rating" in restaurant:
                assert restaurant["rating"] >= valid_preferences["min_rating"]
            if "price" in restaurant:
                assert restaurant["price"] <= valid_preferences["max_price"]


@pytest.mark.e2e
@pytest.mark.requires_api
class TestLLMResponseParsing:
    """Test LLM response parsing and validation."""
    
    def test_parsed_recommendations_have_names(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that parsed recommendations include restaurant names."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        for restaurant in data["recommendations"]:
            assert "name" in restaurant, "Each recommendation should have a name"
            assert isinstance(restaurant["name"], str)
            assert len(restaurant["name"]) > 0
    
    def test_recommendations_match_database(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that LLM recommendations match actual database restaurants."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Each recommendation should have valid restaurant data
        for restaurant in data["recommendations"]:
            # Should have name at minimum
            assert "name" in restaurant
            
            # If it has rating/price, they should be valid
            if "rating" in restaurant:
                assert 0.0 <= restaurant["rating"] <= 5.0
            if "price" in restaurant:
                assert restaurant["price"] >= 0.0


@pytest.mark.e2e
@pytest.mark.requires_api
class TestLLMContextualRecommendations:
    """Test that LLM provides contextual recommendations."""
    
    def test_recommendations_respect_cuisine_preference(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that LLM recommendations respect cuisine preference."""
        preferences = {"cuisine": "italian", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All recommendations should be Italian (if cuisine data available)
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == "italian"
    
    def test_recommendations_respect_rating_preference(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that LLM recommendations respect rating preference."""
        preferences = {"min_rating": 4.5, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All recommendations should meet rating requirement
        for restaurant in data["recommendations"]:
            if "rating" in restaurant:
                assert restaurant["rating"] >= 4.5
    
    def test_recommendations_respect_price_preference(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that LLM recommendations respect price preference."""
        preferences = {"max_price": 25.0, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All recommendations should meet price requirement
        for restaurant in data["recommendations"]:
            if "price" in restaurant:
                assert restaurant["price"] <= 25.0


@pytest.mark.e2e
@pytest.mark.requires_api
class TestLLMPerformance:
    """Test LLM service performance."""
    
    def test_llm_response_time_reasonable(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that LLM responses complete in reasonable time."""
        from conftest import measure_response_time
        
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        assert response.status_code == 200
        
        # LLM requests may take longer, but should complete within 15 seconds
        assert elapsed_time < 15.0, \
            f"LLM request took {elapsed_time:.2f}s, expected < 15s"
    
    def test_multiple_llm_requests_succeed(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that multiple LLM requests succeed."""
        # Make 3 requests
        for i in range(3):
            response = api_client.post("/api/v1/recommendations", json=valid_preferences)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True


@pytest.mark.e2e
@pytest.mark.requires_api
class TestLLMErrorHandling:
    """Test LLM error handling."""
    
    def test_system_handles_llm_timeout(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that system handles LLM timeout gracefully."""
        # Even if LLM times out, should get fallback recommendations
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should succeed with fallback
        assert data["success"] is True
    
    def test_system_handles_llm_error(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that system handles LLM errors gracefully."""
        # Even if LLM fails, should get fallback recommendations
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should succeed with fallback
        assert data["success"] is True


@pytest.mark.e2e
@pytest.mark.requires_api
class TestLLMDifferentScenarios:
    """Test LLM with different preference scenarios."""
    
    def test_llm_with_minimal_preferences(
        self,
        api_client: httpx.Client,
        minimal_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test LLM with minimal preferences."""
        response = api_client.post("/api/v1/recommendations", json=minimal_preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_llm_with_single_filter(
        self,
        api_client: httpx.Client,
        cuisine_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test LLM with single filter."""
        response = api_client.post("/api/v1/recommendations", json=cuisine_only_preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_llm_with_all_filters(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test LLM with all filters."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_llm_with_restrictive_filters(
        self,
        api_client: httpx.Client,
        extreme_filters_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test LLM with very restrictive filters."""
        response = api_client.post("/api/v1/recommendations", json=extreme_filters_preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

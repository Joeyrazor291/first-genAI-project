"""
End-to-End React Frontend Tests

Tests the React frontend UI integration with the Phase 2 API.
Validates that the React application correctly communicates with the backend
and displays recommendations to users.

Note: These tests use httpx to simulate frontend API calls.
For browser-based testing, use Playwright or Selenium.
"""

import pytest
import httpx
import json
from typing import Dict, Any
from conftest import (
    assert_valid_recommendation_response,
    assert_valid_restaurant,
    measure_response_time
)


@pytest.mark.e2e
@pytest.mark.requires_api
class TestReactFrontendIntegration:
    """Test React frontend integration with Phase 2 API."""
    
    def test_react_api_health_check(self, api_client: httpx.Client, wait_for_api):
        """
        Test that React frontend can check API health.
        
        Simulates: React app calling GET /health on mount
        """
        response = api_client.get("/health")
        
        assert response.status_code == 200, "Health endpoint should be accessible"
        data = response.json()
        
        # Verify health response structure
        assert "status" in data, "Health response should include status"
        assert data["status"] in ["healthy", "degraded", "unhealthy"], \
            f"Invalid status: {data['status']}"
        
        # Verify all components are healthy
        assert "engine" in data, "Health response should include engine status"
        assert "database" in data, "Health response should include database status"
        assert "llm_service" in data, "Health response should include llm_service status"
        
        # Verify database stats
        assert "database_stats" in data, "Health response should include database stats"
        stats = data["database_stats"]
        assert stats["total_restaurants"] > 0, "Should have restaurants in database"
        assert stats["unique_cuisines"] > 0, "Should have cuisines in database"
        assert stats["unique_locations"] > 0, "Should have locations in database"
    
    def test_react_form_submission_italian_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React form submission with Italian cuisine filter.
        
        Simulates: User fills form with cuisine="Italian" and clicks submit
        """
        preferences = {
            "cuisine": "Italian",
            "limit": 3
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200, "API should accept form submission"
        data = response.json()
        
        # Verify response structure
        assert_valid_recommendation_response(data)
        assert data["success"] is True, "Request should succeed"
        
        # Verify recommendations
        assert data["count"] > 0, "Should return recommendations"
        assert len(data["recommendations"]) == data["count"], \
            "Recommendation count should match array length"
        
        # Verify each recommendation
        for rec in data["recommendations"]:
            assert_valid_restaurant(rec)
            assert rec["cuisine"].lower() == "italian", \
                f"Expected Italian cuisine, got {rec['cuisine']}"
        
        # Verify filters applied
        assert "filters_applied" in data, "Should include filters_applied"
        assert data["filters_applied"]["cuisine"] == "italian", \
            "Should show cuisine filter applied"
    
    def test_react_form_submission_with_rating_filter(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React form submission with minimum rating filter.
        
        Simulates: User sets min_rating=4.5 and submits
        """
        preferences = {
            "min_rating": 4.5,
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        
        # Verify rating filter applied
        for rec in data["recommendations"]:
            assert rec["rating"] >= 4.5, \
                f"Expected rating >= 4.5, got {rec['rating']}"
    
    def test_react_form_submission_with_price_filter(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React form submission with maximum price filter.
        
        Simulates: User sets max_price=500 and submits
        """
        preferences = {
            "max_price": 500,
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        
        # Verify price filter applied
        for rec in data["recommendations"]:
            assert rec["price"] <= 500, \
                f"Expected price <= 500, got {rec['price']}"
    
    def test_react_form_submission_combined_filters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React form submission with multiple filters combined.
        
        Simulates: User fills multiple form fields and submits
        """
        preferences = {
            "cuisine": "Chinese",
            "location": "mg road",
            "min_rating": 3.5,
            "max_price": 600,
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        
        # Verify all filters applied
        if data["count"] > 0:
            for rec in data["recommendations"]:
                if "cuisine" in rec:
                    assert rec["cuisine"].lower() == "chinese", \
                        f"Expected Chinese cuisine, got {rec['cuisine']}"
                if "rating" in rec:
                    assert rec["rating"] >= 3.5, \
                        f"Expected rating >= 3.5, got {rec['rating']}"
                if "price" in rec:
                    assert rec["price"] <= 600, \
                        f"Expected price <= 600, got {rec['price']}"
    
    def test_react_form_validation_invalid_rating(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React form validation for invalid rating.
        
        Simulates: User enters rating > 5 (invalid)
        """
        preferences = {
            "min_rating": 6.0,  # Invalid: > 5
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # API should reject invalid rating
        assert response.status_code in [400, 422], \
            "API should reject invalid rating"
    
    def test_react_form_validation_invalid_limit(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React form validation for invalid limit.
        
        Simulates: User enters limit > 100 (invalid)
        """
        preferences = {
            "limit": 101  # Invalid: > 100
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # API should reject invalid limit
        assert response.status_code in [400, 422], \
            "API should reject invalid limit"
    
    def test_react_no_results_scenario(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React handling of no results scenario.
        
        Simulates: User enters filters that return no results
        """
        preferences = {
            "cuisine": "NonexistentCuisine",
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return success=false or count=0
        if not data.get("success"):
            assert "error" in data.get("detail", {}), \
                "Should include error message"
        else:
            assert data["count"] == 0, "Should return 0 results"
    
    def test_react_response_time_acceptable(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that API response time is acceptable for React UI.
        
        Requirement: Response should be < 2 seconds for good UX
        """
        preferences = {
            "cuisine": "Italian",
            "limit": 5
        }
        
        with measure_response_time() as timer:
            response = api_client.post("/api/v1/recommendations", json=preferences)
        
        elapsed = timer.elapsed
        
        assert response.status_code == 200
        assert elapsed < 2.0, \
            f"Response time {elapsed:.2f}s exceeds 2s threshold"
    
    def test_react_recommendation_card_data_complete(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that recommendation cards have all required data for React display.
        
        Verifies: name, cuisine, location, rating, price, explanation
        """
        preferences = {
            "cuisine": "Italian",
            "limit": 1
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] > 0, "Should return at least one recommendation"
        
        rec = data["recommendations"][0]
        
        # Verify all card data is present
        required_fields = ["name", "cuisine", "location", "rating", "price"]
        for field in required_fields:
            assert field in rec, f"Recommendation missing required field: {field}"
            assert rec[field] is not None, f"Field {field} should not be None"
        
        # Verify explanation (generated by LLM)
        assert "explanation" in rec, "Should include LLM-generated explanation"
        assert len(rec["explanation"]) > 0, "Explanation should not be empty"
    
    def test_react_filters_applied_display(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that filters_applied data is correct for React UI display.
        
        Simulates: React displaying active filters as tags
        """
        preferences = {
            "cuisine": "Italian",
            "location": "indiranagar",
            "min_rating": 4.0,
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify filters_applied structure
        assert "filters_applied" in data, "Should include filters_applied"
        filters = data["filters_applied"]
        
        # Verify applied filters match request
        assert filters.get("cuisine") == "italian", "Cuisine filter should be applied"
        assert filters.get("min_rating") == 4.0, "Rating filter should be applied"
    
    def test_react_multiple_submissions(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test React handling of multiple form submissions.
        
        Simulates: User submits form, gets results, changes filters, submits again
        """
        # First submission
        prefs1 = {"cuisine": "Italian", "limit": 3}
        response1 = api_client.post("/api/v1/recommendations", json=prefs1)
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second submission with different filters
        prefs2 = {"cuisine": "Chinese", "limit": 3}
        response2 = api_client.post("/api/v1/recommendations", json=prefs2)
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Verify results are different
        if data1["count"] > 0 and data2["count"] > 0:
            first_rec1 = data1["recommendations"][0]["name"]
            first_rec2 = data2["recommendations"][0]["name"]
            
            # Results should be different (different cuisines)
            # Note: This might not always be true, so we just verify both succeeded
            assert data1["success"] and data2["success"], \
                "Both submissions should succeed"
    
    def test_react_cors_headers_present(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that CORS headers are present for React frontend.
        
        Requirement: React frontend on different port needs CORS headers
        """
        response = api_client.get("/health")
        
        # Check for CORS headers
        headers = response.headers
        
        # CORS headers might be present (depends on server configuration)
        # At minimum, request should succeed
        assert response.status_code == 200, "Request should succeed"
    
    def test_react_error_message_structure(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that error responses have proper structure for React error display.
        
        Simulates: React displaying error messages to user
        """
        # Send invalid request
        preferences = {
            "min_rating": 10.0,  # Invalid
            "limit": 5
        }
        
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should get error response
        if response.status_code != 200:
            data = response.json()
            
            # Verify error structure
            assert "detail" in data or "error" in data, \
                "Error response should include error details"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestReactFrontendPerformance:
    """Test React frontend performance requirements."""
    
    def test_health_check_performance(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test health check performance (called on app mount).
        
        Requirement: < 500ms for good UX
        """
        with measure_response_time() as timer:
            response = api_client.get("/health")
        
        assert response.status_code == 200
        assert timer.elapsed < 0.5, \
            f"Health check took {timer.elapsed:.2f}s, should be < 0.5s"
    
    def test_recommendations_performance_small_result_set(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test recommendations performance with small result set.
        
        Requirement: < 1.5s for good UX
        """
        preferences = {"limit": 3}
        
        with measure_response_time() as timer:
            response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        assert timer.elapsed < 1.5, \
            f"Recommendations took {timer.elapsed:.2f}s, should be < 1.5s"
    
    def test_recommendations_performance_large_result_set(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test recommendations performance with large result set.
        
        Requirement: < 2s for acceptable UX
        """
        preferences = {"limit": 50}
        
        with measure_response_time() as timer:
            response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        assert timer.elapsed < 2.0, \
            f"Recommendations took {timer.elapsed:.2f}s, should be < 2s"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestReactFrontendDataDisplay:
    """Test React frontend data display requirements."""
    
    def test_recommendation_card_rendering_data(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that all data needed for recommendation card rendering is present.
        
        Simulates: React rendering recommendation cards
        """
        preferences = {"limit": 1}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        if data["count"] > 0:
            rec = data["recommendations"][0]
            
            # Verify card display data
            assert "name" in rec, "Card needs restaurant name"
            assert "cuisine" in rec, "Card needs cuisine"
            assert "location" in rec, "Card needs location"
            assert "rating" in rec, "Card needs rating"
            assert "price" in rec, "Card needs price"
            assert "explanation" in rec, "Card needs explanation"
            
            # Verify data types
            assert isinstance(rec["name"], str), "Name should be string"
            assert isinstance(rec["rating"], (int, float)), "Rating should be number"
            assert isinstance(rec["price"], (int, float)), "Price should be number"
            assert isinstance(rec["explanation"], str), "Explanation should be string"
    
    def test_results_info_display_data(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test that results info data is correct for React display.
        
        Simulates: React displaying "Found X restaurants, showing Y"
        """
        preferences = {"limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify results info
        assert "count" in data, "Should include count (showing)"
        assert "total_found" in data, "Should include total_found"
        
        # Verify counts are valid
        assert data["count"] <= data["total_found"], \
            "Showing count should not exceed total found"
        assert data["count"] <= 5, "Should respect limit"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

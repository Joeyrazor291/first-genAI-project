"""
End-to-End API Endpoint Tests

Comprehensive tests for all REST API endpoints including request/response
validation, HTTP status codes, headers, and CORS.
"""

import pytest
import httpx
from typing import Dict, Any
from conftest import (
    assert_valid_recommendation_response,
    assert_valid_stats_response,
    measure_response_time
)


@pytest.mark.e2e
@pytest.mark.requires_api
class TestRootEndpoint:
    """Test root endpoint functionality."""
    
    def test_root_endpoint_returns_api_info(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that root endpoint returns API information."""
        response = api_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "name" in data, "Response should include API name"
        assert "version" in data, "Response should include API version"
        assert "status" in data, "Response should include status"
        assert "endpoints" in data, "Response should include endpoints"
        
        # Verify status
        assert data["status"] == "running", "API should be running"
        
        # Verify endpoints are listed
        endpoints = data["endpoints"]
        assert isinstance(endpoints, dict), "Endpoints should be a dictionary"
        assert len(endpoints) > 0, "Should list available endpoints"
    
    def test_root_endpoint_response_time(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that root endpoint responds quickly."""
        response, elapsed_time = measure_response_time(api_client.get, "/")
        
        assert response.status_code == 200
        assert elapsed_time < 1.0, f"Root endpoint took {elapsed_time:.2f}s, expected < 1s"
    
    def test_root_endpoint_headers(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that root endpoint returns correct headers."""
        response = api_client.get("/")
        
        assert response.status_code == 200
        
        # Check content type
        assert "application/json" in response.headers.get("content-type", ""), \
            "Response should be JSON"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestHealthEndpoint:
    """Test health check endpoint functionality."""
    
    def test_health_check_returns_healthy_status(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that health check returns healthy status."""
        response = api_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify status field
        assert "status" in data, "Health check should include status"
        assert data["status"] in ["healthy", "degraded"], \
            f"Status should be healthy or degraded, got {data['status']}"
        
        # Verify component health
        assert "database" in data, "Should include database health"
        assert "engine" in data, "Should include engine health"
    
    def test_health_check_database_connectivity(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that health check verifies database connectivity."""
        response = api_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Database should be connected
        assert data.get("database") in ["connected", "healthy"], \
            f"Database should be connected, got {data.get('database')}"
        
        # Should include database stats
        if "database_stats" in data:
            stats = data["database_stats"]
            assert "total_restaurants" in stats
            assert stats["total_restaurants"] > 0, "Database should contain restaurants"
    
    def test_health_check_response_time(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that health check responds quickly."""
        response, elapsed_time = measure_response_time(api_client.get, "/health")
        
        assert response.status_code == 200
        assert elapsed_time < 2.0, f"Health check took {elapsed_time:.2f}s, expected < 2s"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestRecommendationsEndpoint:
    """Test recommendations endpoint functionality."""
    
    def test_recommendations_endpoint_accepts_post(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that recommendations endpoint accepts POST requests."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        assert_valid_recommendation_response(response.json())
    
    def test_recommendations_endpoint_rejects_get(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that recommendations endpoint rejects GET requests."""
        response = api_client.get("/api/v1/recommendations")
        
        # Should return 405 Method Not Allowed or 404
        assert response.status_code in [404, 405], \
            f"GET should not be allowed, got {response.status_code}"
    
    def test_recommendations_endpoint_requires_json(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that recommendations endpoint requires JSON content type."""
        response = api_client.post(
            "/api/v1/recommendations",
            data="not json",
            headers={"Content-Type": "text/plain"}
        )
        
        # Should return 400 or 422 for invalid content type
        assert response.status_code in [400, 422], \
            f"Non-JSON should be rejected, got {response.status_code}"
    
    def test_recommendations_endpoint_validates_input(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that recommendations endpoint validates input."""
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        # Should return 400 or 422 for invalid input
        assert response.status_code in [400, 422], \
            f"Invalid input should be rejected, got {response.status_code}"
    
    def test_recommendations_endpoint_response_structure(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that recommendations endpoint returns correct structure."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        assert "success" in data
        assert "recommendations" in data
        assert "filters_applied" in data
        assert "count" in data or "returned" in data
        
        # Verify types
        assert isinstance(data["success"], bool)
        assert isinstance(data["recommendations"], list)
        assert isinstance(data["filters_applied"], dict)
    
    def test_recommendations_endpoint_empty_results(
        self,
        api_client: httpx.Client,
        nonexistent_cuisine_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test recommendations endpoint with no matching results."""
        response = api_client.post("/api/v1/recommendations", json=nonexistent_cuisine_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert len(data["recommendations"]) == 0
        count = data.get("count") or data.get("returned", 0)
        assert count == 0


@pytest.mark.e2e
@pytest.mark.requires_api
class TestRestaurantsEndpoint:
    """Test restaurants listing endpoint functionality."""
    
    def test_restaurants_endpoint_lists_all(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that restaurants endpoint lists all restaurants."""
        response = api_client.get("/api/v1/restaurants")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "success" in data
        assert "count" in data
        assert "restaurants" in data
        
        assert data["success"] is True
        assert isinstance(data["restaurants"], list)
        assert data["count"] == len(data["restaurants"])
    
    def test_restaurants_endpoint_respects_limit(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that restaurants endpoint respects limit parameter."""
        limit = 5
        response = api_client.get(f"/api/v1/restaurants?limit={limit}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["restaurants"]) <= limit, \
            f"Expected max {limit} restaurants, got {len(data['restaurants'])}"
    
    def test_restaurants_endpoint_default_limit(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that restaurants endpoint uses default limit."""
        response = api_client.get("/api/v1/restaurants")
        
        assert response.status_code == 200
        data = response.json()
        
        # Default limit should be 50
        assert len(data["restaurants"]) <= 50, \
            f"Expected max 50 restaurants (default), got {len(data['restaurants'])}"
    
    def test_restaurants_endpoint_max_limit_cap(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that restaurants endpoint caps limit at 100."""
        response = api_client.get("/api/v1/restaurants?limit=200")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be capped at 100
        assert len(data["restaurants"]) <= 100, \
            f"Expected max 100 restaurants (cap), got {len(data['restaurants'])}"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestStatsEndpoint:
    """Test statistics endpoint functionality."""
    
    def test_stats_endpoint_returns_statistics(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that stats endpoint returns database statistics."""
        response = api_client.get("/api/v1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_stats_response(data)
    
    def test_stats_endpoint_values_are_positive(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that stats endpoint returns positive values."""
        response = api_client.get("/api/v1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_restaurants"] > 0, "Should have restaurants in database"
        assert data["unique_cuisines"] > 0, "Should have cuisines in database"
        assert data["unique_locations"] > 0, "Should have locations in database"
    
    def test_stats_endpoint_consistency(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that stats endpoint returns consistent values."""
        # Call twice and compare
        response1 = api_client.get("/api/v1/stats")
        response2 = api_client.get("/api/v1/stats")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Values should be identical (database hasn't changed)
        assert data1["total_restaurants"] == data2["total_restaurants"]
        assert data1["unique_cuisines"] == data2["unique_cuisines"]
        assert data1["unique_locations"] == data2["unique_locations"]


@pytest.mark.e2e
@pytest.mark.requires_api
class TestCORSHeaders:
    """Test CORS headers on all endpoints."""
    
    def test_cors_headers_on_recommendations(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that recommendations endpoint includes CORS headers."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        
        # Check for CORS headers
        headers = response.headers
        assert "access-control-allow-origin" in headers, "Should include CORS origin header"
    
    def test_cors_preflight_request(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test CORS preflight OPTIONS request."""
        response = api_client.options(
            "/api/v1/recommendations",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Should allow OPTIONS request
        assert response.status_code in [200, 204], \
            f"OPTIONS should be allowed, got {response.status_code}"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestErrorResponses:
    """Test error response formats."""
    
    def test_404_for_invalid_endpoint(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that invalid endpoints return 404."""
        response = api_client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
    
    def test_error_response_format(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that error responses have consistent format."""
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        assert response.status_code in [400, 422]
        data = response.json()
        
        # Should include error details
        assert "detail" in data or "error" in data, "Error response should include details"
    
    def test_malformed_json_error(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test error response for malformed JSON."""
        response = api_client.post(
            "/api/v1/recommendations",
            content="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        
        # Should return 400 or 422 for malformed JSON
        assert response.status_code in [400, 422], \
            f"Malformed JSON should be rejected, got {response.status_code}"

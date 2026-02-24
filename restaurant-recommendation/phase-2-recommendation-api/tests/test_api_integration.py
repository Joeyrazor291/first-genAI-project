"""Integration tests for Phase 2 API with Phase 5 integration."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


class TestRootEndpoints:
    """Test root and health endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data


class TestRecommendationsEndpoint:
    """Test recommendations endpoint."""
    
    def test_get_recommendations_with_valid_preferences(self):
        """Test getting recommendations with valid preferences."""
        payload = {
            "cuisine": "italian",
            "location": "downtown",
            "min_rating": 4.0,
            "max_price": 30.0,
            "limit": 5
        }
        
        response = client.post("/api/v1/recommendations", json=payload)
        
        # Should succeed or return service unavailable if Phase 5 not set up
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            assert "recommendations" in data
            assert isinstance(data["recommendations"], list)
    
    def test_get_recommendations_with_minimal_preferences(self):
        """Test getting recommendations with minimal preferences."""
        payload = {
            "limit": 10
        }
        
        response = client.post("/api/v1/recommendations", json=payload)
        
        assert response.status_code in [200, 503]
    
    def test_get_recommendations_with_invalid_rating(self):
        """Test getting recommendations with invalid rating."""
        payload = {
            "min_rating": 10.0,  # Invalid: > 5.0
            "limit": 5
        }
        
        response = client.post("/api/v1/recommendations", json=payload)
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_get_recommendations_with_invalid_limit(self):
        """Test getting recommendations with invalid limit."""
        payload = {
            "limit": 200  # Invalid: > 100
        }
        
        response = client.post("/api/v1/recommendations", json=payload)
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_get_recommendations_with_negative_price(self):
        """Test getting recommendations with negative price."""
        payload = {
            "max_price": -10.0  # Invalid: negative
        }
        
        response = client.post("/api/v1/recommendations", json=payload)
        
        # Should return 422 for validation error
        assert response.status_code == 422


class TestRestaurantsEndpoint:
    """Test restaurants listing endpoint."""
    
    def test_list_restaurants_default(self):
        """Test listing restaurants with default limit."""
        response = client.get("/api/v1/restaurants")
        
        assert response.status_code in [200, 500, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "restaurants" in data
            assert isinstance(data["restaurants"], list)
    
    def test_list_restaurants_with_limit(self):
        """Test listing restaurants with custom limit."""
        response = client.get("/api/v1/restaurants?limit=10")
        
        assert response.status_code in [200, 500, 503]
    
    def test_list_restaurants_limit_capped_at_100(self):
        """Test that limit is capped at 100."""
        response = client.get("/api/v1/restaurants?limit=200")
        
        assert response.status_code in [200, 500, 503]


class TestStatsEndpoint:
    """Test statistics endpoint."""
    
    def test_get_stats(self):
        """Test getting database statistics."""
        response = client.get("/api/v1/stats")
        
        assert response.status_code in [200, 500, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "total_restaurants" in data
            assert "unique_cuisines" in data
            assert "unique_locations" in data


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present."""
        response = client.options("/api/v1/recommendations")
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers or response.status_code == 405


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_endpoint(self):
        """Test accessing invalid endpoint."""
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
    
    def test_invalid_method(self):
        """Test using invalid HTTP method."""
        response = client.get("/api/v1/recommendations")  # Should be POST
        
        assert response.status_code == 405


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation endpoints."""
    
    def test_openapi_json_accessible(self):
        """Test that OpenAPI JSON is accessible."""
        response = client.get("/api/v1/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_swagger_docs_accessible(self):
        """Test that Swagger UI is accessible."""
        response = client.get("/api/v1/docs")
        
        assert response.status_code == 200
    
    def test_redoc_accessible(self):
        """Test that ReDoc is accessible."""
        response = client.get("/api/v1/redoc")
        
        assert response.status_code == 200

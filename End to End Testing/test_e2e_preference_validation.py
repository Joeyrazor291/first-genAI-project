"""
End-to-End Preference Validation Tests

Tests for user preference validation, normalization, and error handling
through the complete API flow.
"""

import pytest
import httpx
from typing import Dict, Any


@pytest.mark.e2e
@pytest.mark.requires_api
class TestPreferenceValidation:
    """Test preference validation through API."""
    
    def test_valid_all_preferences(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that all valid preferences are accepted."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_invalid_rating_too_high(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that rating > 5.0 is rejected."""
        preferences = {"min_rating": 6.0}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
    
    def test_invalid_rating_negative(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that negative rating is rejected."""
        preferences = {"min_rating": -1.0}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
    
    def test_invalid_price_negative(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that negative price is rejected."""
        preferences = {"max_price": -10.0}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
    
    def test_invalid_limit_zero(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that limit of 0 is rejected."""
        preferences = {"limit": 0}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
    
    def test_invalid_limit_too_high(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that limit > 100 is rejected."""
        preferences = {"limit": 150}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
    
    def test_invalid_limit_negative(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that negative limit is rejected."""
        preferences = {"limit": -5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]


@pytest.mark.e2e
@pytest.mark.requires_api
class TestPreferenceNormalization:
    """Test preference normalization through API."""
    
    def test_cuisine_normalized_to_lowercase(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that cuisine is normalized to lowercase."""
        preferences = {"cuisine": "ITALIAN", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check filters_applied shows normalized value
        filters = data.get("filters_applied", {})
        if "cuisine" in filters:
            assert filters["cuisine"] == "italian", "Cuisine should be normalized to lowercase"
    
    def test_location_normalized_to_lowercase(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that location is normalized to lowercase."""
        preferences = {"location": "DOWNTOWN", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check filters_applied shows normalized value
        filters = data.get("filters_applied", {})
        if "location" in filters:
            assert filters["location"] == "downtown", "Location should be normalized to lowercase"
    
    def test_whitespace_trimmed_from_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that whitespace is trimmed from cuisine."""
        preferences = {"cuisine": "  italian  ", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        filters = data.get("filters_applied", {})
        if "cuisine" in filters:
            assert filters["cuisine"] == "italian", "Whitespace should be trimmed"
    
    def test_whitespace_trimmed_from_location(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that whitespace is trimmed from location."""
        preferences = {"location": "  downtown  ", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        filters = data.get("filters_applied", {})
        if "location" in filters:
            assert filters["location"] == "downtown", "Whitespace should be trimmed"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestBoundaryValues:
    """Test boundary value handling."""
    
    def test_rating_minimum_boundary(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test minimum rating boundary (0.0)."""
        preferences = {"min_rating": 0.0, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_rating_maximum_boundary(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test maximum rating boundary (5.0)."""
        preferences = {"min_rating": 5.0, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_price_minimum_boundary(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test minimum price boundary (0.0)."""
        preferences = {"max_price": 0.0, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_limit_minimum_boundary(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test minimum limit boundary (1)."""
        preferences = {"limit": 1}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        count = data.get("count") or data.get("returned", 0)
        assert count <= 1, "Should respect limit of 1"
    
    def test_limit_maximum_boundary(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test maximum limit boundary (100)."""
        preferences = {"limit": 100}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        count = data.get("count") or data.get("returned", 0)
        assert count <= 100, "Should respect limit of 100"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestDefaultValues:
    """Test default value application."""
    
    def test_default_limit_applied(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that default limit (10) is applied when not specified."""
        preferences = {"cuisine": "italian"}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        count = data.get("count") or data.get("returned", 0)
        assert count <= 10, "Should use default limit of 10"
    
    def test_no_filters_uses_defaults(
        self,
        api_client: httpx.Client,
        empty_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that empty preferences uses all defaults."""
        response = api_client.post("/api/v1/recommendations", json=empty_preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Should return results with defaults
        count = data.get("count") or data.get("returned", 0)
        assert count > 0, "Should return results with default filters"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestOptionalFields:
    """Test optional field handling."""
    
    def test_cuisine_optional(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that cuisine is optional."""
        preferences = {"location": "downtown", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_location_optional(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that location is optional."""
        preferences = {"cuisine": "italian", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_min_rating_optional(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that min_rating is optional."""
        preferences = {"cuisine": "italian", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_max_price_optional(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that max_price is optional."""
        preferences = {"cuisine": "italian", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


@pytest.mark.e2e
@pytest.mark.requires_api
class TestTypeConversion:
    """Test type conversion and coercion."""
    
    def test_rating_as_integer(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that integer rating is accepted and converted."""
        preferences = {"min_rating": 4, "limit": 5}  # Integer instead of float
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_price_as_integer(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that integer price is accepted and converted."""
        preferences = {"max_price": 30, "limit": 5}  # Integer instead of float
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


@pytest.mark.e2e
@pytest.mark.requires_api
class TestErrorMessages:
    """Test error message clarity and accuracy."""
    
    def test_error_message_for_invalid_rating(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that invalid rating returns clear error message."""
        preferences = {"min_rating": 10.0}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
        data = response.json()
        
        # Should include error details
        assert "detail" in data or "error" in data
    
    def test_error_message_for_invalid_limit(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that invalid limit returns clear error message."""
        preferences = {"limit": 200}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code in [400, 422]
        data = response.json()
        
        # Should include error details
        assert "detail" in data or "error" in data

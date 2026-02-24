"""
End-to-End Database Integration Tests

Tests for database connectivity, query accuracy, filter combinations,
and data integrity through the complete API flow.
"""

import pytest
import httpx
from typing import Dict, Any
from conftest import assert_valid_restaurant


@pytest.mark.e2e
@pytest.mark.requires_api
class TestDatabaseConnectivity:
    """Test database connectivity through API."""
    
    def test_database_accessible_via_health_check(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that database is accessible via health check."""
        response = api_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data.get("database") in ["connected", "healthy"], \
            "Database should be connected"
    
    def test_database_contains_data(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that database contains restaurant data."""
        response = api_client.get("/api/v1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_restaurants"] > 0, "Database should contain restaurants"
        assert data["unique_cuisines"] > 0, "Database should contain cuisines"
        assert data["unique_locations"] > 0, "Database should contain locations"
    
    def test_database_query_returns_results(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that database queries return results."""
        preferences = {"limit": 10}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        count = data.get("count") or data.get("returned", 0)
        assert count > 0, "Database query should return results"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestQueryAccuracy:
    """Test accuracy of database queries."""
    
    def test_cuisine_filter_accuracy(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that cuisine filter returns only matching restaurants."""
        preferences = {"cuisine": "italian", "limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should be Italian cuisine
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == "italian", \
                    f"Expected Italian, got {restaurant['cuisine']}"
    
    def test_location_filter_accuracy(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that location filter returns only matching restaurants."""
        preferences = {"location": "downtown", "limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should be in downtown
        for restaurant in data["recommendations"]:
            if "location" in restaurant:
                assert restaurant["location"] == "downtown", \
                    f"Expected downtown, got {restaurant['location']}"
    
    def test_rating_filter_accuracy(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that rating filter returns only matching restaurants."""
        min_rating = 4.0
        preferences = {"min_rating": min_rating, "limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should have rating >= min_rating
        for restaurant in data["recommendations"]:
            if "rating" in restaurant:
                assert restaurant["rating"] >= min_rating, \
                    f"Expected rating >= {min_rating}, got {restaurant['rating']}"
    
    def test_price_filter_accuracy(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that price filter returns only matching restaurants."""
        max_price = 25.0
        preferences = {"max_price": max_price, "limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should have price <= max_price
        for restaurant in data["recommendations"]:
            if "price" in restaurant:
                assert restaurant["price"] <= max_price, \
                    f"Expected price <= {max_price}, got {restaurant['price']}"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestFilterCombinations:
    """Test combinations of multiple filters."""
    
    def test_cuisine_and_location_filters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test combination of cuisine and location filters."""
        preferences = {
            "cuisine": "italian",
            "location": "downtown",
            "limit": 20
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should match both filters
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == "italian"
            if "location" in restaurant:
                assert restaurant["location"] == "downtown"
    
    def test_cuisine_and_rating_filters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test combination of cuisine and rating filters."""
        preferences = {
            "cuisine": "italian",
            "min_rating": 4.0,
            "limit": 20
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should match both filters
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == "italian"
            if "rating" in restaurant:
                assert restaurant["rating"] >= 4.0
    
    def test_all_filters_combined(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test all filters combined."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should match all filters
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == valid_preferences["cuisine"]
            if "location" in restaurant:
                assert restaurant["location"] == valid_preferences["location"]
            if "rating" in restaurant:
                assert restaurant["rating"] >= valid_preferences["min_rating"]
            if "price" in restaurant:
                assert restaurant["price"] <= valid_preferences["max_price"]
    
    def test_rating_and_price_filters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test combination of rating and price filters."""
        preferences = {
            "min_rating": 4.0,
            "max_price": 30.0,
            "limit": 20
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should match both filters
        for restaurant in data["recommendations"]:
            if "rating" in restaurant:
                assert restaurant["rating"] >= 4.0
            if "price" in restaurant:
                assert restaurant["price"] <= 30.0


@pytest.mark.e2e
@pytest.mark.requires_api
class TestDataIntegrity:
    """Test data integrity and consistency."""
    
    def test_restaurant_data_structure(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that all restaurants have valid data structure."""
        preferences = {"limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate each restaurant
        for restaurant in data["recommendations"]:
            # Skip enriched recommendations (with explanation only)
            if "explanation" in restaurant and "rating" not in restaurant:
                continue
            
            # Validate regular restaurant data
            if "rating" in restaurant:
                assert_valid_restaurant(restaurant)
    
    def test_no_duplicate_restaurants(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that results don't contain duplicate restaurants."""
        preferences = {"limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check for duplicates by name
        names = [r.get("name") for r in data["recommendations"] if "name" in r]
        unique_names = set(names)
        
        assert len(names) == len(unique_names), "Results should not contain duplicates"
    
    def test_rating_values_in_range(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that all ratings are in valid range [0.0, 5.0]."""
        preferences = {"limit": 50}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        for restaurant in data["recommendations"]:
            if "rating" in restaurant:
                rating = restaurant["rating"]
                assert 0.0 <= rating <= 5.0, \
                    f"Rating {rating} out of valid range [0.0, 5.0]"
    
    def test_price_values_non_negative(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that all prices are non-negative."""
        preferences = {"limit": 50}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        for restaurant in data["recommendations"]:
            if "price" in restaurant:
                price = restaurant["price"]
                assert price >= 0.0, f"Price {price} should be non-negative"
    
    def test_text_fields_not_empty(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that text fields are not empty."""
        preferences = {"limit": 20}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        for restaurant in data["recommendations"]:
            if "name" in restaurant:
                assert len(restaurant["name"].strip()) > 0, "Name should not be empty"
            if "cuisine" in restaurant:
                assert len(restaurant["cuisine"].strip()) > 0, "Cuisine should not be empty"
            if "location" in restaurant:
                assert len(restaurant["location"].strip()) > 0, "Location should not be empty"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestQueryPerformance:
    """Test database query performance."""
    
    def test_simple_query_performance(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that simple queries complete quickly."""
        from conftest import measure_response_time
        
        preferences = {"cuisine": "italian", "limit": 10}
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 5.0, \
            f"Simple query took {elapsed_time:.2f}s, expected < 5s"
    
    def test_complex_query_performance(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that complex queries with multiple filters complete reasonably."""
        from conftest import measure_response_time
        
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 10.0, \
            f"Complex query took {elapsed_time:.2f}s, expected < 10s"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestEdgeCaseQueries:
    """Test edge case database queries."""
    
    def test_query_with_no_results(
        self,
        api_client: httpx.Client,
        nonexistent_cuisine_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test query that returns no results."""
        response = api_client.post("/api/v1/recommendations", json=nonexistent_cuisine_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        count = data.get("count") or data.get("returned", 0)
        assert count == 0
        assert len(data["recommendations"]) == 0
    
    def test_query_with_very_restrictive_filters(
        self,
        api_client: httpx.Client,
        extreme_filters_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test query with very restrictive filters."""
        response = api_client.post("/api/v1/recommendations", json=extreme_filters_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should succeed even if no results
        assert data["success"] is True
    
    def test_query_with_limit_one(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test query with limit of 1."""
        preferences = {"limit": 1}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        count = data.get("count") or data.get("returned", 0)
        assert count <= 1
        assert len(data["recommendations"]) <= 1

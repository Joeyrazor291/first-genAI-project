"""Tests for API endpoints."""

import pytest
from fastapi import status


class TestRootEndpoint:
    """Test cases for root endpoint."""
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint returns API information."""
        response = test_client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'name' in data
        assert 'version' in data
        assert 'status' in data
        assert data['status'] == 'running'


class TestHealthEndpoint:
    """Test cases for health check endpoint."""
    
    def test_health_check_success(self, test_client):
        """Test health check returns healthy status."""
        response = test_client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['database'] == 'connected'
        assert 'restaurants_count' in data


class TestRecommendationsEndpoint:
    """Test cases for recommendations endpoint."""
    
    def test_get_recommendations_with_all_filters(self, test_client, valid_preferences):
        """Test getting recommendations with all filters."""
        response = test_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        assert 'count' in data
        assert 'recommendations' in data
        assert 'filters_applied' in data
        assert isinstance(data['recommendations'], list)
    
    def test_get_recommendations_minimal_filters(self, test_client, minimal_preferences):
        """Test getting recommendations with minimal filters."""
        response = test_client.post("/api/v1/recommendations", json=minimal_preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        assert data['count'] > 0
        assert len(data['recommendations']) <= 10  # Default limit
    
    def test_get_recommendations_by_cuisine(self, test_client):
        """Test filtering by cuisine."""
        preferences = {"cuisine": "italian", "limit": 10}
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # All results should be Italian
        for restaurant in data['recommendations']:
            assert restaurant['cuisine'] == 'italian'
    
    def test_get_recommendations_by_location(self, test_client):
        """Test filtering by location."""
        preferences = {"location": "downtown", "limit": 10}
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # All results should be in downtown
        for restaurant in data['recommendations']:
            assert restaurant['location'] == 'downtown'
    
    def test_get_recommendations_by_min_rating(self, test_client):
        """Test filtering by minimum rating."""
        preferences = {"min_rating": 4.5, "limit": 10}
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # All results should have rating >= 4.5
        for restaurant in data['recommendations']:
            assert restaurant['rating'] >= 4.5
    
    def test_get_recommendations_by_max_price(self, test_client):
        """Test filtering by maximum price."""
        preferences = {"max_price": 25.0, "limit": 10}
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # All results should have price <= 25.0
        for restaurant in data['recommendations']:
            assert restaurant['price'] <= 25.0
    
    def test_get_recommendations_combined_filters(self, test_client):
        """Test with multiple filters combined."""
        preferences = {
            "cuisine": "italian",
            "min_rating": 4.0,
            "max_price": 30.0,
            "limit": 5
        }
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify all filters are applied
        for restaurant in data['recommendations']:
            assert restaurant['cuisine'] == 'italian'
            assert restaurant['rating'] >= 4.0
            assert restaurant['price'] <= 30.0
        
        # Verify limit
        assert len(data['recommendations']) <= 5
    
    def test_get_recommendations_no_matches(self, test_client):
        """Test when no restaurants match the criteria."""
        preferences = {
            "cuisine": "nonexistent",
            "limit": 10
        }
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        assert data['count'] == 0
        assert len(data['recommendations']) == 0
    
    def test_get_recommendations_invalid_rating(self, test_client, invalid_preferences_rating):
        """Test with invalid rating value."""
        response = test_client.post("/api/v1/recommendations", json=invalid_preferences_rating)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_recommendations_invalid_price(self, test_client, invalid_preferences_price):
        """Test with invalid price value."""
        response = test_client.post("/api/v1/recommendations", json=invalid_preferences_price)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_recommendations_invalid_limit(self, test_client, invalid_preferences_limit):
        """Test with invalid limit value."""
        response = test_client.post("/api/v1/recommendations", json=invalid_preferences_limit)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_recommendations_respects_limit(self, test_client):
        """Test that limit parameter is respected."""
        preferences = {"limit": 3}
        response = test_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['recommendations']) <= 3


class TestRestaurantsEndpoint:
    """Test cases for restaurants listing endpoint."""
    
    def test_list_restaurants(self, test_client):
        """Test listing all restaurants."""
        response = test_client.get("/api/v1/restaurants")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        assert 'count' in data
        assert 'restaurants' in data
        assert isinstance(data['restaurants'], list)
    
    def test_list_restaurants_with_limit(self, test_client):
        """Test listing restaurants with limit."""
        response = test_client.get("/api/v1/restaurants?limit=5")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['restaurants']) <= 5
    
    def test_list_restaurants_limit_capped_at_100(self, test_client):
        """Test that limit is capped at 100."""
        response = test_client.get("/api/v1/restaurants?limit=200")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['restaurants']) <= 100


class TestStatsEndpoint:
    """Test cases for statistics endpoint."""
    
    def test_get_stats(self, test_client):
        """Test getting database statistics."""
        response = test_client.get("/api/v1/stats")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'total_restaurants' in data
        assert 'unique_cuisines' in data
        assert 'unique_locations' in data
        assert data['total_restaurants'] > 0
        assert data['unique_cuisines'] > 0
        assert data['unique_locations'] > 0
    
    def test_stats_values_are_correct(self, test_client):
        """Test that statistics values are accurate."""
        response = test_client.get("/api/v1/stats")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Based on our test data (12 restaurants)
        assert data['total_restaurants'] == 12
        assert data['unique_cuisines'] > 0
        assert data['unique_locations'] == 3  # Downtown, Uptown, Midtown


class TestResponseModels:
    """Test cases for response model validation."""
    
    def test_recommendation_response_structure(self, test_client, valid_preferences):
        """Test that recommendation response has correct structure."""
        response = test_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check required fields
        assert 'success' in data
        assert 'count' in data
        assert 'recommendations' in data
        assert 'filters_applied' in data
        
        # Check restaurant structure
        if data['count'] > 0:
            restaurant = data['recommendations'][0]
            assert 'name' in restaurant
            assert 'cuisine' in restaurant
            assert 'location' in restaurant
            assert 'rating' in restaurant
            assert 'price' in restaurant
    
    def test_stats_response_structure(self, test_client):
        """Test that stats response has correct structure."""
        response = test_client.get("/api/v1/stats")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check required fields
        assert 'total_restaurants' in data
        assert 'unique_cuisines' in data
        assert 'unique_locations' in data
        
        # Check types
        assert isinstance(data['total_restaurants'], int)
        assert isinstance(data['unique_cuisines'], int)
        assert isinstance(data['unique_locations'], int)

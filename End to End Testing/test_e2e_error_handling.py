"""
End-to-End Error Handling Tests

Tests for error scenarios, edge cases, service failures, and graceful degradation.
"""

import pytest
import httpx
from typing import Dict, Any


@pytest.mark.e2e
@pytest.mark.requires_api
class TestInvalidInputHandling:
    """Test handling of invalid inputs."""
    
    def test_invalid_json_format(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of malformed JSON."""
        response = api_client.post(
            "/api/v1/recommendations",
            content="{invalid: json}",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 422]
    
    def test_empty_json_body(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of empty JSON body."""
        response = api_client.post(
            "/api/v1/recommendations",
            json={}
        )
        
        # Empty body should be accepted (uses defaults)
        assert response.status_code == 200
    
    def test_null_values_in_preferences(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of null values in preferences."""
        preferences = {
            "cuisine": None,
            "location": None,
            "min_rating": None,
            "max_price": None,
            "limit": 10
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle null values gracefully
        assert response.status_code == 200
    
    def test_wrong_data_types(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of wrong data types."""
        preferences = {
            "cuisine": 123,  # Should be string
            "min_rating": "not a number",  # Should be float
            "limit": "five"  # Should be int
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should reject with validation error
        assert response.status_code in [400, 422]
    
    def test_extra_unexpected_fields(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of extra unexpected fields."""
        preferences = {
            "cuisine": "italian",
            "limit": 5,
            "unexpected_field": "should be ignored",
            "another_field": 123
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should accept and ignore extra fields
        assert response.status_code == 200
    
    def test_empty_string_values(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of empty string values."""
        preferences = {
            "cuisine": "",
            "location": "",
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Empty strings should be handled (treated as not provided)
        assert response.status_code in [200, 400, 422]
    
    def test_whitespace_only_strings(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of whitespace-only strings."""
        preferences = {
            "cuisine": "   ",
            "location": "\t\n",
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Whitespace-only should be handled
        assert response.status_code in [200, 400, 422]


@pytest.mark.e2e
@pytest.mark.requires_api
class TestHTTPErrorCodes:
    """Test HTTP error code responses."""
    
    def test_404_for_nonexistent_endpoint(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test 404 for non-existent endpoint."""
        response = api_client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
    
    def test_405_for_wrong_http_method(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test 405 for wrong HTTP method."""
        response = api_client.get("/api/v1/recommendations")
        
        # Should return 404 or 405
        assert response.status_code in [404, 405]
    
    def test_400_for_validation_errors(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test 400/422 for validation errors."""
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        assert response.status_code in [400, 422]
    
    def test_error_response_includes_details(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that error responses include details."""
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        assert response.status_code in [400, 422]
        data = response.json()
        
        # Should include error information
        assert "detail" in data or "error" in data


@pytest.mark.e2e
@pytest.mark.requires_api
class TestEdgeCaseScenarios:
    """Test edge case scenarios."""
    
    def test_very_long_cuisine_name(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of very long cuisine name."""
        preferences = {
            "cuisine": "a" * 1000,  # 1000 character cuisine name
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle gracefully (likely no results)
        assert response.status_code == 200
    
    def test_special_characters_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of special characters in cuisine."""
        preferences = {
            "cuisine": "italian@#$%",
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_unicode_characters_in_preferences(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of unicode characters."""
        preferences = {
            "cuisine": "中文",
            "location": "日本",
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle unicode gracefully
        assert response.status_code == 200
    
    def test_sql_injection_attempt_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that SQL injection attempts are handled safely."""
        preferences = {
            "cuisine": "italian'; DROP TABLE restaurants; --",
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle safely (no SQL injection)
        assert response.status_code == 200
        
        # Verify database still works
        stats_response = api_client.get("/api/v1/stats")
        assert stats_response.status_code == 200
    
    def test_xss_attempt_in_preferences(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that XSS attempts are handled safely."""
        preferences = {
            "cuisine": "<script>alert('xss')</script>",
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle safely
        assert response.status_code == 200
    
    def test_extremely_high_rating(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of extremely high rating value."""
        preferences = {
            "min_rating": 999999.0,
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should reject as invalid
        assert response.status_code in [400, 422]
    
    def test_extremely_high_price(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of extremely high price value."""
        preferences = {
            "max_price": 999999999.0,
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should accept (valid, just very high)
        assert response.status_code == 200
    
    def test_negative_infinity_values(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of negative infinity."""
        preferences = {
            "min_rating": float('-inf'),
            "limit": 5
        }
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should reject or handle gracefully
        assert response.status_code in [200, 400, 422]


@pytest.mark.e2e
@pytest.mark.requires_api
class TestConcurrentRequests:
    """Test handling of concurrent requests."""
    
    @pytest.mark.asyncio
    async def test_multiple_concurrent_requests(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test handling of multiple concurrent requests."""
        import asyncio
        
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            # Send 5 concurrent requests
            tasks = [
                client.post("/api/v1/recommendations", json=valid_preferences)
                for _ in range(5)
            ]
            
            responses = await asyncio.gather(*tasks)
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
    
    @pytest.mark.asyncio
    async def test_concurrent_different_requests(
        self,
        api_base_url: str,
        wait_for_api
    ):
        """Test handling of different concurrent requests."""
        import asyncio
        
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            # Send different types of requests concurrently
            tasks = [
                client.get("/health"),
                client.get("/api/v1/stats"),
                client.post("/api/v1/recommendations", json={"cuisine": "italian"}),
                client.post("/api/v1/recommendations", json={"location": "downtown"}),
                client.get("/api/v1/restaurants?limit=10")
            ]
            
            responses = await asyncio.gather(*tasks)
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.requires_api
class TestGracefulDegradation:
    """Test graceful degradation scenarios."""
    
    def test_no_results_handled_gracefully(
        self,
        api_client: httpx.Client,
        nonexistent_cuisine_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that no results scenario is handled gracefully."""
        response = api_client.post("/api/v1/recommendations", json=nonexistent_cuisine_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert len(data["recommendations"]) == 0
        # Should include helpful message or empty list
    
    def test_partial_data_handled_gracefully(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that partial/incomplete data is handled gracefully."""
        # Request with only one filter
        preferences = {"cuisine": "italian"}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


@pytest.mark.e2e
@pytest.mark.requires_api
class TestTimeoutScenarios:
    """Test timeout and slow response scenarios."""
    
    def test_request_with_short_timeout(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test request with very short timeout."""
        # Create client with 0.001 second timeout
        with httpx.Client(base_url=api_base_url, timeout=0.001) as client:
            try:
                response = client.post("/api/v1/recommendations", json=valid_preferences)
                # If it succeeds, that's fine (very fast response)
                assert response.status_code == 200
            except httpx.TimeoutException:
                # Timeout is expected with such short timeout
                pass
    
    def test_request_with_reasonable_timeout(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test request with reasonable timeout."""
        # Create client with 30 second timeout
        with httpx.Client(base_url=api_base_url, timeout=30.0) as client:
            response = client.post("/api/v1/recommendations", json=valid_preferences)
            
            # Should complete within timeout
            assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.requires_api
class TestResponseConsistency:
    """Test response consistency across multiple requests."""
    
    def test_same_request_consistent_results(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that same request returns consistent results."""
        # Make same request twice
        response1 = api_client.post("/api/v1/recommendations", json=valid_preferences)
        response2 = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Count should be consistent
        count1 = data1.get("count") or data1.get("returned", 0)
        count2 = data2.get("count") or data2.get("returned", 0)
        
        # Results should be similar (may vary if LLM is involved)
        # At minimum, counts should be close
        assert abs(count1 - count2) <= 2, "Results should be consistent"

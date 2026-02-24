"""
End-to-End Performance Tests

Tests for response times, concurrent request handling, database query performance,
and system scalability.
"""

import pytest
import httpx
import asyncio
from typing import Dict, Any
from conftest import measure_response_time


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.slow
class TestResponseTimes:
    """Test API response times."""
    
    def test_health_check_response_time(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that health check responds quickly."""
        response, elapsed_time = measure_response_time(api_client.get, "/health")
        
        assert response.status_code == 200
        assert elapsed_time < 2.0, \
            f"Health check took {elapsed_time:.2f}s, expected < 2s"
        
        print(f"\n✓ Health check: {elapsed_time:.3f}s")
    
    def test_stats_endpoint_response_time(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that stats endpoint responds quickly."""
        response, elapsed_time = measure_response_time(api_client.get, "/api/v1/stats")
        
        assert response.status_code == 200
        assert elapsed_time < 2.0, \
            f"Stats endpoint took {elapsed_time:.2f}s, expected < 2s"
        
        print(f"\n✓ Stats endpoint: {elapsed_time:.3f}s")
    
    def test_simple_recommendation_response_time(
        self,
        api_client: httpx.Client,
        cuisine_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test simple recommendation request response time."""
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=cuisine_only_preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 5.0, \
            f"Simple recommendation took {elapsed_time:.2f}s, expected < 5s"
        
        print(f"\n✓ Simple recommendation: {elapsed_time:.3f}s")
    
    def test_complex_recommendation_response_time(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test complex recommendation request response time."""
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 10.0, \
            f"Complex recommendation took {elapsed_time:.2f}s, expected < 10s"
        
        print(f"\n✓ Complex recommendation: {elapsed_time:.3f}s")
    
    def test_list_restaurants_response_time(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test list restaurants endpoint response time."""
        response, elapsed_time = measure_response_time(
            api_client.get,
            "/api/v1/restaurants?limit=50"
        )
        
        assert response.status_code == 200
        assert elapsed_time < 3.0, \
            f"List restaurants took {elapsed_time:.2f}s, expected < 3s"
        
        print(f"\n✓ List restaurants: {elapsed_time:.3f}s")


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.slow
class TestConcurrentRequestHandling:
    """Test handling of concurrent requests."""
    
    @pytest.mark.asyncio
    async def test_concurrent_health_checks(
        self,
        api_base_url: str,
        wait_for_api
    ):
        """Test multiple concurrent health check requests."""
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            # Send 10 concurrent health checks
            tasks = [client.get("/health") for _ in range(10)]
            
            import time
            start_time = time.time()
            responses = await asyncio.gather(*tasks)
            elapsed_time = time.time() - start_time
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200
            
            # Should complete reasonably fast
            assert elapsed_time < 5.0, \
                f"10 concurrent health checks took {elapsed_time:.2f}s, expected < 5s"
            
            print(f"\n✓ 10 concurrent health checks: {elapsed_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_recommendation_requests(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test multiple concurrent recommendation requests."""
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            # Send 5 concurrent recommendation requests
            tasks = [
                client.post("/api/v1/recommendations", json=valid_preferences)
                for _ in range(5)
            ]
            
            import time
            start_time = time.time()
            responses = await asyncio.gather(*tasks)
            elapsed_time = time.time() - start_time
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
            
            # Should complete within reasonable time
            assert elapsed_time < 30.0, \
                f"5 concurrent recommendations took {elapsed_time:.2f}s, expected < 30s"
            
            print(f"\n✓ 5 concurrent recommendations: {elapsed_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_mixed_requests(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test concurrent requests of different types."""
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            # Mix of different request types
            tasks = [
                client.get("/health"),
                client.get("/api/v1/stats"),
                client.post("/api/v1/recommendations", json=valid_preferences),
                client.post("/api/v1/recommendations", json={"cuisine": "italian"}),
                client.get("/api/v1/restaurants?limit=10"),
                client.get("/health"),
                client.post("/api/v1/recommendations", json={"location": "downtown"}),
            ]
            
            import time
            start_time = time.time()
            responses = await asyncio.gather(*tasks)
            elapsed_time = time.time() - start_time
            
            # All should succeed
            for response in responses:
                assert response.status_code == 200
            
            print(f"\n✓ 7 concurrent mixed requests: {elapsed_time:.3f}s")


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.slow
class TestDatabaseQueryPerformance:
    """Test database query performance."""
    
    def test_simple_filter_query_performance(
        self,
        api_client: httpx.Client,
        cuisine_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test performance of simple filter query."""
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=cuisine_only_preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 5.0, \
            f"Simple filter query took {elapsed_time:.2f}s, expected < 5s"
    
    def test_multiple_filter_query_performance(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test performance of query with multiple filters."""
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 10.0, \
            f"Multiple filter query took {elapsed_time:.2f}s, expected < 10s"
    
    def test_large_result_set_performance(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test performance when requesting large result set."""
        preferences = {"limit": 100}
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=preferences
        )
        
        assert response.status_code == 200
        assert elapsed_time < 10.0, \
            f"Large result set query took {elapsed_time:.2f}s, expected < 10s"
    
    def test_stats_query_performance(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test performance of stats aggregation query."""
        response, elapsed_time = measure_response_time(
            api_client.get,
            "/api/v1/stats"
        )
        
        assert response.status_code == 200
        assert elapsed_time < 2.0, \
            f"Stats query took {elapsed_time:.2f}s, expected < 2s"


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.slow
class TestSequentialRequestPerformance:
    """Test performance of sequential requests."""
    
    def test_sequential_recommendation_requests(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test performance of 10 sequential recommendation requests."""
        import time
        
        start_time = time.time()
        
        for i in range(10):
            response = api_client.post("/api/v1/recommendations", json=valid_preferences)
            assert response.status_code == 200
        
        elapsed_time = time.time() - start_time
        avg_time = elapsed_time / 10
        
        print(f"\n✓ 10 sequential requests: {elapsed_time:.3f}s (avg: {avg_time:.3f}s)")
        
        # Average should be reasonable
        assert avg_time < 5.0, \
            f"Average request time {avg_time:.2f}s, expected < 5s"
    
    def test_sequential_different_requests(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test performance of sequential different requests."""
        import time
        
        requests = [
            ("GET", "/health", None),
            ("GET", "/api/v1/stats", None),
            ("POST", "/api/v1/recommendations", {"cuisine": "italian"}),
            ("POST", "/api/v1/recommendations", {"location": "downtown"}),
            ("GET", "/api/v1/restaurants?limit=10", None),
        ]
        
        start_time = time.time()
        
        for method, url, json_data in requests:
            if method == "GET":
                response = api_client.get(url)
            else:
                response = api_client.post(url, json=json_data)
            
            assert response.status_code == 200
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✓ 5 sequential different requests: {elapsed_time:.3f}s")
        
        assert elapsed_time < 20.0, \
            f"Sequential requests took {elapsed_time:.2f}s, expected < 20s"


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.slow
class TestCachingAndOptimization:
    """Test caching and optimization effects."""
    
    def test_repeated_identical_requests(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test performance of repeated identical requests."""
        # First request (cold)
        response1, time1 = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        # Second request (potentially cached)
        response2, time2 = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        # Third request
        response3, time3 = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        
        print(f"\n✓ Request times: {time1:.3f}s, {time2:.3f}s, {time3:.3f}s")
    
    def test_stats_caching(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test stats endpoint caching/optimization."""
        # Multiple stats requests
        times = []
        
        for i in range(5):
            response, elapsed_time = measure_response_time(
                api_client.get,
                "/api/v1/stats"
            )
            assert response.status_code == 200
            times.append(elapsed_time)
        
        avg_time = sum(times) / len(times)
        print(f"\n✓ Stats requests avg time: {avg_time:.3f}s")
        
        # All should be fast
        for t in times:
            assert t < 2.0, f"Stats request took {t:.2f}s, expected < 2s"


@pytest.mark.e2e
@pytest.mark.requires_api
@pytest.mark.slow
class TestLoadScenarios:
    """Test system under various load scenarios."""
    
    @pytest.mark.asyncio
    async def test_burst_load(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test system under burst load (many requests at once)."""
        async with httpx.AsyncClient(base_url=api_base_url, timeout=60.0) as client:
            # Send 20 concurrent requests
            tasks = [
                client.post("/api/v1/recommendations", json=valid_preferences)
                for _ in range(20)
            ]
            
            import time
            start_time = time.time()
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            elapsed_time = time.time() - start_time
            
            # Count successes
            successes = sum(
                1 for r in responses
                if not isinstance(r, Exception) and r.status_code == 200
            )
            
            print(f"\n✓ Burst load: {successes}/20 succeeded in {elapsed_time:.3f}s")
            
            # At least 80% should succeed
            assert successes >= 16, f"Only {successes}/20 requests succeeded"
    
    @pytest.mark.asyncio
    async def test_sustained_load(
        self,
        api_base_url: str,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test system under sustained load."""
        async with httpx.AsyncClient(base_url=api_base_url, timeout=60.0) as client:
            # Send requests in batches
            total_requests = 0
            total_successes = 0
            
            import time
            start_time = time.time()
            
            for batch in range(3):
                tasks = [
                    client.post("/api/v1/recommendations", json=valid_preferences)
                    for _ in range(5)
                ]
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                successes = sum(
                    1 for r in responses
                    if not isinstance(r, Exception) and r.status_code == 200
                )
                
                total_requests += 5
                total_successes += successes
                
                # Small delay between batches
                await asyncio.sleep(0.5)
            
            elapsed_time = time.time() - start_time
            
            print(f"\n✓ Sustained load: {total_successes}/{total_requests} succeeded in {elapsed_time:.3f}s")
            
            # At least 80% should succeed
            assert total_successes >= 12, f"Only {total_successes}/15 requests succeeded"

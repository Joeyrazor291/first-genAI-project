"""
End-to-End Complete Flow Tests

Tests the complete user journey from preference input through all phases
to final recommendations. Validates data flow across all system components.
"""

import pytest
import httpx
from typing import Dict, Any
from conftest import (
    assert_valid_recommendation_response,
    assert_valid_restaurant,
    assert_filters_applied,
    measure_response_time
)


@pytest.mark.e2e
@pytest.mark.requires_api
class TestCompleteUserJourney:
    """Test complete user journey from input to recommendations."""
    
    def test_complete_flow_with_all_filters(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test complete flow: User provides all filters and receives recommendations.
        
        This validates:
        1. API accepts request
        2. Preferences are validated (Phase 3)
        3. Database is queried (Phase 1)
        4. LLM generates recommendations (Phase 4)
        5. Response is properly formatted
        """
        # Step 1: Submit preferences
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        # Step 2: Verify successful response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        # Step 3: Validate response structure
        assert_valid_recommendation_response(data)
        assert data["success"] is True, "Request should succeed"
        
        # Step 4: Verify filters were applied
        assert_filters_applied(data, {
            "cuisine": "italian",
            "min_rating": 4.0,
            "limit": 5
        })
        
        # Step 5: Verify recommendations match filters
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == "italian", \
                    f"Expected Italian cuisine, got {restaurant['cuisine']}"
            if "rating" in restaurant:
                assert restaurant["rating"] >= 4.0, \
                    f"Expected rating >= 4.0, got {restaurant['rating']}"
            if "price" in restaurant:
                assert restaurant["price"] <= 30.0, \
                    f"Expected price <= 30.0, got {restaurant['price']}"
        
        # Step 6: Verify limit is respected
        count = data.get("count") or data.get("returned", 0)
        assert count <= 5, f"Expected max 5 results, got {count}"
    
    def test_complete_flow_minimal_input(
        self,
        api_client: httpx.Client,
        minimal_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test complete flow with minimal input (defaults applied).
        
        Validates that the system applies appropriate defaults when
        user provides minimal preferences.
        """
        response = api_client.post("/api/v1/recommendations", json=minimal_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Should return results with default limit (10)
        count = data.get("count") or data.get("returned", 0)
        assert count <= 10, f"Expected max 10 results (default), got {count}"
    
    def test_complete_flow_empty_preferences(
        self,
        api_client: httpx.Client,
        empty_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test complete flow with empty preferences.
        
        System should apply all defaults and return general recommendations.
        """
        response = api_client.post("/api/v1/recommendations", json=empty_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Should return some results
        count = data.get("count") or data.get("returned", 0)
        assert count > 0, "Should return recommendations with default filters"
    
    def test_complete_flow_single_filter_cuisine(
        self,
        api_client: httpx.Client,
        cuisine_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test complete flow with only cuisine filter."""
        response = api_client.post("/api/v1/recommendations", json=cuisine_only_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Verify cuisine filter was applied
        for restaurant in data["recommendations"]:
            if "cuisine" in restaurant:
                assert restaurant["cuisine"] == "italian"
    
    def test_complete_flow_single_filter_location(
        self,
        api_client: httpx.Client,
        location_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test complete flow with only location filter."""
        response = api_client.post("/api/v1/recommendations", json=location_only_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Verify location filter was applied
        for restaurant in data["recommendations"]:
            if "location" in restaurant:
                assert restaurant["location"] == "downtown"
    
    def test_complete_flow_single_filter_rating(
        self,
        api_client: httpx.Client,
        rating_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test complete flow with only rating filter."""
        response = api_client.post("/api/v1/recommendations", json=rating_only_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Verify rating filter was applied
        for restaurant in data["recommendations"]:
            if "rating" in restaurant:
                assert restaurant["rating"] >= 4.5
    
    def test_complete_flow_single_filter_price(
        self,
        api_client: httpx.Client,
        price_only_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test complete flow with only price filter."""
        response = api_client.post("/api/v1/recommendations", json=price_only_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Verify price filter was applied
        for restaurant in data["recommendations"]:
            if "price" in restaurant:
                assert restaurant["price"] <= 25.0


@pytest.mark.e2e
@pytest.mark.requires_api
class TestMultiStepWorkflows:
    """Test multi-step user workflows."""
    
    def test_workflow_refine_search(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test workflow: User refines search progressively.
        
        Simulates user starting broad and narrowing down preferences.
        """
        # Step 1: Broad search
        response1 = api_client.post("/api/v1/recommendations", json={"limit": 10})
        assert response1.status_code == 200
        data1 = response1.json()
        count1 = data1.get("count") or data1.get("returned", 0)
        
        # Step 2: Add cuisine filter
        response2 = api_client.post("/api/v1/recommendations", json={
            "cuisine": "italian",
            "limit": 10
        })
        assert response2.status_code == 200
        data2 = response2.json()
        count2 = data2.get("count") or data2.get("returned", 0)
        
        # Step 3: Add rating filter
        response3 = api_client.post("/api/v1/recommendations", json={
            "cuisine": "italian",
            "min_rating": 4.0,
            "limit": 10
        })
        assert response3.status_code == 200
        data3 = response3.json()
        count3 = data3.get("count") or data3.get("returned", 0)
        
        # Verify results narrow down (or stay same if already filtered)
        assert count2 <= count1 or count1 == 0, "Adding filter should narrow or maintain results"
        assert count3 <= count2 or count2 == 0, "Adding more filters should narrow or maintain results"
    
    def test_workflow_compare_locations(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test workflow: User compares restaurants in different locations.
        
        Simulates user exploring options in multiple areas.
        """
        locations = ["downtown", "uptown", "midtown"]
        results = {}
        
        for location in locations:
            response = api_client.post("/api/v1/recommendations", json={
                "location": location,
                "min_rating": 4.0,
                "limit": 5
            })
            
            assert response.status_code == 200
            data = response.json()
            results[location] = data.get("count") or data.get("returned", 0)
        
        # Verify we got results for at least one location
        assert sum(results.values()) > 0, "Should find restaurants in at least one location"
    
    def test_workflow_explore_cuisines(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test workflow: User explores different cuisine types.
        
        Simulates user browsing various cuisine options.
        """
        cuisines = ["italian", "chinese", "mexican", "indian"]
        results = {}
        
        for cuisine in cuisines:
            response = api_client.post("/api/v1/recommendations", json={
                "cuisine": cuisine,
                "limit": 5
            })
            
            assert response.status_code == 200
            data = response.json()
            results[cuisine] = data.get("count") or data.get("returned", 0)
        
        # Verify we got results for at least one cuisine
        assert sum(results.values()) > 0, "Should find restaurants for at least one cuisine"


@pytest.mark.e2e
@pytest.mark.requires_api
class TestDataFlowValidation:
    """Test data flow across all system phases."""
    
    def test_data_flow_phase1_to_phase2(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """
        Test data flow from Phase 1 (Database) to Phase 2 (API).
        
        Validates that database data is correctly exposed through API.
        """
        # Get stats to verify database connectivity
        stats_response = api_client.get("/api/v1/stats")
        assert stats_response.status_code == 200
        stats = stats_response.json()
        
        assert stats["total_restaurants"] > 0, "Database should contain restaurants"
        
        # Get recommendations to verify data retrieval
        rec_response = api_client.post("/api/v1/recommendations", json={"limit": 5})
        assert rec_response.status_code == 200
        data = rec_response.json()
        
        count = data.get("count") or data.get("returned", 0)
        assert count > 0, "Should retrieve restaurants from database"
    
    def test_data_flow_phase3_validation(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test data flow through Phase 3 (Preference Processing).
        
        Validates that invalid preferences are caught and rejected.
        """
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        # Should reject invalid input
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for invalid input, got {response.status_code}"
    
    def test_data_flow_complete_pipeline(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test complete data flow through all phases.
        
        Validates:
        - Phase 2: API receives request
        - Phase 3: Preferences validated
        - Phase 1: Database queried
        - Phase 5: Engine orchestrates
        - Phase 4: LLM generates (if available)
        - Phase 2: Response returned
        """
        response, elapsed_time = measure_response_time(
            api_client.post,
            "/api/v1/recommendations",
            json=valid_preferences
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate complete response
        assert_valid_recommendation_response(data)
        assert data["success"] is True
        
        # Verify reasonable response time (< 10 seconds)
        assert elapsed_time < 10.0, \
            f"Response took {elapsed_time:.2f}s, expected < 10s"
        
        print(f"\n✓ Complete pipeline executed in {elapsed_time:.2f}s")


@pytest.mark.e2e
@pytest.mark.requires_api
class TestEdgeCaseFlows:
    """Test edge case scenarios in complete flows."""
    
    def test_flow_no_matching_restaurants(
        self,
        api_client: httpx.Client,
        nonexistent_cuisine_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test flow when no restaurants match criteria.
        
        System should handle gracefully with empty results.
        """
        response = api_client.post("/api/v1/recommendations", json=nonexistent_cuisine_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        count = data.get("count") or data.get("returned", 0)
        assert count == 0, "Should return 0 results for non-existent cuisine"
        assert len(data["recommendations"]) == 0
    
    def test_flow_extremely_restrictive_filters(
        self,
        api_client: httpx.Client,
        extreme_filters_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test flow with extremely restrictive filters.
        
        May return few or no results, but should not error.
        """
        response = api_client.post("/api/v1/recommendations", json=extreme_filters_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        # May have 0 results, which is valid
        assert "recommendations" in data
    
    def test_flow_boundary_values(
        self,
        api_client: httpx.Client,
        boundary_preferences: Dict[str, Any],
        wait_for_api
    ):
        """
        Test flow with boundary values (min/max allowed).
        
        System should handle edge values correctly.
        """
        response = api_client.post("/api/v1/recommendations", json=boundary_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        # Verify limit of 1 is respected
        count = data.get("count") or data.get("returned", 0)
        assert count <= 1, "Should respect limit of 1"

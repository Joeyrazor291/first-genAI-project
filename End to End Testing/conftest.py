"""
Shared fixtures and configuration for end-to-end tests.

This module provides common test fixtures, utilities, and configuration
used across all E2E test files.
"""

import pytest
import sys
from pathlib import Path
import httpx
import time
from typing import Dict, Any, Generator

# Add project paths
project_root = Path(__file__).parent.parent / "restaurant-recommendation"
sys.path.insert(0, str(project_root / "phase-1-data-pipeline"))
sys.path.insert(0, str(project_root / "phase-2-recommendation-api"))
sys.path.insert(0, str(project_root / "phase-3-preference-processing" / "src"))
sys.path.insert(0, str(project_root / "phase-4-llm-integration" / "src"))
sys.path.insert(0, str(project_root / "phase-5-recommendation-engine" / "src"))


# Test Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_DELAY = 1.0


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL for API server."""
    return API_BASE_URL


@pytest.fixture(scope="session")
def api_client() -> Generator[httpx.Client, None, None]:
    """
    HTTP client for API requests.
    
    Yields:
        httpx.Client configured for API testing
    """
    with httpx.Client(base_url=API_BASE_URL, timeout=API_TIMEOUT) as client:
        yield client


@pytest.fixture(scope="session")
async def async_api_client() -> Generator[httpx.AsyncClient, None, None]:
    """
    Async HTTP client for concurrent API requests.
    
    Yields:
        httpx.AsyncClient configured for API testing
    """
    async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=API_TIMEOUT) as client:
        yield client


@pytest.fixture(scope="session")
def wait_for_api(api_client: httpx.Client) -> None:
    """
    Wait for API server to be ready before running tests.
    
    Args:
        api_client: HTTP client fixture
        
    Raises:
        RuntimeError: If API server is not available after retries
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = api_client.get("/health")
            if response.status_code == 200:
                print(f"\n✓ API server is ready")
                return
        except httpx.ConnectError:
            if attempt < MAX_RETRIES - 1:
                print(f"\n⏳ Waiting for API server (attempt {attempt + 1}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY)
            else:
                raise RuntimeError(
                    f"API server not available at {API_BASE_URL}. "
                    "Please start the server: cd restaurant-recommendation/phase-2-recommendation-api && python src/main.py"
                )


@pytest.fixture
def valid_preferences() -> Dict[str, Any]:
    """Valid user preferences for testing."""
    return {
        "cuisine": "italian",
        "location": "downtown",
        "min_rating": 4.0,
        "max_price": 30.0,
        "limit": 5
    }


@pytest.fixture
def minimal_preferences() -> Dict[str, Any]:
    """Minimal valid preferences (only required fields)."""
    return {
        "limit": 10
    }


@pytest.fixture
def cuisine_only_preferences() -> Dict[str, Any]:
    """Preferences with only cuisine filter."""
    return {
        "cuisine": "italian"
    }


@pytest.fixture
def location_only_preferences() -> Dict[str, Any]:
    """Preferences with only location filter."""
    return {
        "location": "downtown"
    }


@pytest.fixture
def rating_only_preferences() -> Dict[str, Any]:
    """Preferences with only rating filter."""
    return {
        "min_rating": 4.5
    }


@pytest.fixture
def price_only_preferences() -> Dict[str, Any]:
    """Preferences with only price filter."""
    return {
        "max_price": 25.0
    }


@pytest.fixture
def boundary_preferences() -> Dict[str, Any]:
    """Preferences with boundary values."""
    return {
        "min_rating": 5.0,  # Maximum rating
        "max_price": 0.01,  # Minimum price
        "limit": 1  # Minimum limit
    }


@pytest.fixture
def invalid_rating_preferences() -> Dict[str, Any]:
    """Preferences with invalid rating (out of range)."""
    return {
        "cuisine": "italian",
        "min_rating": 6.0  # Invalid: > 5.0
    }


@pytest.fixture
def invalid_price_preferences() -> Dict[str, Any]:
    """Preferences with invalid price (negative)."""
    return {
        "cuisine": "italian",
        "max_price": -10.0  # Invalid: negative
    }


@pytest.fixture
def invalid_limit_preferences() -> Dict[str, Any]:
    """Preferences with invalid limit (out of range)."""
    return {
        "cuisine": "italian",
        "limit": 200  # Invalid: > 100
    }


@pytest.fixture
def empty_preferences() -> Dict[str, Any]:
    """Empty preferences dictionary."""
    return {}


@pytest.fixture
def nonexistent_cuisine_preferences() -> Dict[str, Any]:
    """Preferences with non-existent cuisine."""
    return {
        "cuisine": "klingon",
        "limit": 10
    }


@pytest.fixture
def nonexistent_location_preferences() -> Dict[str, Any]:
    """Preferences with non-existent location."""
    return {
        "location": "atlantis",
        "limit": 10
    }


@pytest.fixture
def extreme_filters_preferences() -> Dict[str, Any]:
    """Preferences with extremely restrictive filters."""
    return {
        "cuisine": "italian",
        "location": "downtown",
        "min_rating": 4.9,
        "max_price": 5.0,
        "limit": 100
    }


def assert_valid_restaurant(restaurant: Dict[str, Any]) -> None:
    """
    Assert that a restaurant object has valid structure and values.
    
    Args:
        restaurant: Restaurant dictionary to validate
        
    Raises:
        AssertionError: If restaurant structure is invalid
    """
    # Check required fields exist
    assert "name" in restaurant, "Restaurant missing 'name' field"
    assert "cuisine" in restaurant, "Restaurant missing 'cuisine' field"
    assert "location" in restaurant, "Restaurant missing 'location' field"
    assert "rating" in restaurant, "Restaurant missing 'rating' field"
    assert "price" in restaurant, "Restaurant missing 'price' field"
    
    # Check field types
    assert isinstance(restaurant["name"], str), "Restaurant name must be string"
    assert isinstance(restaurant["cuisine"], str), "Restaurant cuisine must be string"
    assert isinstance(restaurant["location"], str), "Restaurant location must be string"
    assert isinstance(restaurant["rating"], (int, float)), "Restaurant rating must be numeric"
    assert isinstance(restaurant["price"], (int, float)), "Restaurant price must be numeric"
    
    # Check value ranges
    assert 0.0 <= restaurant["rating"] <= 5.0, f"Rating {restaurant['rating']} out of range [0.0, 5.0]"
    assert restaurant["price"] >= 0.0, f"Price {restaurant['price']} must be non-negative"
    
    # Check non-empty strings
    assert len(restaurant["name"].strip()) > 0, "Restaurant name cannot be empty"
    assert len(restaurant["cuisine"].strip()) > 0, "Restaurant cuisine cannot be empty"
    assert len(restaurant["location"].strip()) > 0, "Restaurant location cannot be empty"


def assert_valid_recommendation_response(response_data: Dict[str, Any]) -> None:
    """
    Assert that a recommendation response has valid structure.
    
    Args:
        response_data: Response dictionary to validate
        
    Raises:
        AssertionError: If response structure is invalid
    """
    # Check required fields
    assert "success" in response_data, "Response missing 'success' field"
    assert "count" in response_data or "returned" in response_data, "Response missing count field"
    assert "recommendations" in response_data, "Response missing 'recommendations' field"
    assert "filters_applied" in response_data, "Response missing 'filters_applied' field"
    
    # Check types
    assert isinstance(response_data["success"], bool), "success must be boolean"
    assert isinstance(response_data["recommendations"], list), "recommendations must be list"
    assert isinstance(response_data["filters_applied"], dict), "filters_applied must be dict"
    
    # Validate each recommendation
    for restaurant in response_data["recommendations"]:
        # Check if it's an enriched recommendation (with explanation) or regular restaurant
        if "explanation" in restaurant:
            # Enriched recommendation
            assert isinstance(restaurant["explanation"], str), "explanation must be string"
            assert len(restaurant["explanation"]) > 0, "explanation cannot be empty"
        else:
            # Regular restaurant - validate structure
            assert_valid_restaurant(restaurant)


def assert_valid_stats_response(response_data: Dict[str, Any]) -> None:
    """
    Assert that a stats response has valid structure.
    
    Args:
        response_data: Stats response dictionary to validate
        
    Raises:
        AssertionError: If stats structure is invalid
    """
    # Check required fields
    assert "total_restaurants" in response_data, "Stats missing 'total_restaurants'"
    assert "unique_cuisines" in response_data, "Stats missing 'unique_cuisines'"
    assert "unique_locations" in response_data, "Stats missing 'unique_locations'"
    
    # Check types and values
    assert isinstance(response_data["total_restaurants"], int), "total_restaurants must be int"
    assert isinstance(response_data["unique_cuisines"], int), "unique_cuisines must be int"
    assert isinstance(response_data["unique_locations"], int), "unique_locations must be int"
    
    assert response_data["total_restaurants"] >= 0, "total_restaurants must be non-negative"
    assert response_data["unique_cuisines"] >= 0, "unique_cuisines must be non-negative"
    assert response_data["unique_locations"] >= 0, "unique_locations must be non-negative"


def assert_filters_applied(
    response_data: Dict[str, Any],
    expected_filters: Dict[str, Any]
) -> None:
    """
    Assert that the correct filters were applied in the response.
    
    Args:
        response_data: Response dictionary containing filters_applied
        expected_filters: Expected filter values
        
    Raises:
        AssertionError: If filters don't match expectations
    """
    filters_applied = response_data.get("filters_applied", {})
    
    for key, expected_value in expected_filters.items():
        if expected_value is not None:
            assert key in filters_applied, f"Filter '{key}' not in filters_applied"
            assert filters_applied[key] == expected_value, \
                f"Filter '{key}' expected {expected_value}, got {filters_applied[key]}"


def measure_response_time(func, *args, **kwargs) -> tuple:
    """
    Measure execution time of a function.
    
    Args:
        func: Function to measure
        *args: Positional arguments for function
        **kwargs: Keyword arguments for function
        
    Returns:
        Tuple of (result, elapsed_time_seconds)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return result, elapsed_time


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "requires_llm: marks tests that require LLM service"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API server running"
    )

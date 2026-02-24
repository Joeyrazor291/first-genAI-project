"""Shared test fixtures for Phase 2 tests."""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
import pandas as pd

# Add Phase 1 to path
phase1_path = Path(__file__).parent.parent.parent / 'phase-1-data-pipeline'
sys.path.insert(0, str(phase1_path))

from src.data.store import RestaurantStore
from src.data.preprocessing import clean_restaurant_data


@pytest.fixture
def sample_restaurants_data():
    """Fixture providing sample restaurant data."""
    data = {
        'Name': [
            'Bella Italia', 'Dragon Palace', 'Taco Fiesta', 'Curry House',
            'Le Bistro', 'Sushi Master', 'Pizza Roma', 'Thai Garden',
            'Burger Joint', 'Pasta Paradise', 'Spice Route', 'Noodle Bar'
        ],
        'Cuisine': [
            'Italian', 'Chinese', 'Mexican', 'Indian',
            'French', 'Japanese', 'Italian', 'Thai',
            'American', 'Italian', 'Indian', 'Chinese'
        ],
        'Location': [
            'Downtown', 'Uptown', 'Midtown', 'Downtown',
            'Uptown', 'Downtown', 'Midtown', 'Uptown',
            'Downtown', 'Midtown', 'Downtown', 'Uptown'
        ],
        'Rating': [4.5, 4.2, 4.0, 4.7, 4.8, 4.6, 4.3, 4.4, 3.9, 4.5, 4.6, 4.1],
        'Price': [25.50, 18.00, 12.50, 22.00, 45.00, 35.00, 20.00, 28.00, 15.00, 30.00, 24.00, 16.00]
    }
    return pd.DataFrame(data)


@pytest.fixture
def test_db_path(tmp_path):
    """Fixture providing a temporary test database path."""
    return tmp_path / "test_restaurant.db"


@pytest.fixture
def populated_test_db(test_db_path, sample_restaurants_data):
    """Fixture providing a populated test database."""
    # Clean the data
    cleaned_df = clean_restaurant_data(sample_restaurants_data)
    
    # Create and populate database
    store = RestaurantStore(db_path=test_db_path)
    store.create_tables()
    store.store_restaurants(cleaned_df)
    store.close()
    
    return test_db_path


@pytest.fixture
def test_client(populated_test_db):
    """Fixture providing a FastAPI test client with test database."""
    # Import here to avoid circular imports
    from src.api import app
    from src.database import db_service
    
    # Override database path
    db_service.db_path = populated_test_db
    db_service._store = None  # Reset store to use new path
    
    client = TestClient(app)
    yield client
    
    # Cleanup
    db_service.close()


@pytest.fixture
def valid_preferences():
    """Fixture providing valid user preferences."""
    return {
        "cuisine": "italian",
        "location": "downtown",
        "min_rating": 4.0,
        "max_price": 30.0,
        "limit": 5
    }


@pytest.fixture
def minimal_preferences():
    """Fixture providing minimal user preferences."""
    return {}


@pytest.fixture
def invalid_preferences_rating():
    """Fixture providing invalid preferences (bad rating)."""
    return {
        "min_rating": 6.0  # Invalid: > 5.0
    }


@pytest.fixture
def invalid_preferences_price():
    """Fixture providing invalid preferences (negative price)."""
    return {
        "max_price": -10.0  # Invalid: negative
    }


@pytest.fixture
def invalid_preferences_limit():
    """Fixture providing invalid preferences (bad limit)."""
    return {
        "limit": 200  # Invalid: > 100
    }

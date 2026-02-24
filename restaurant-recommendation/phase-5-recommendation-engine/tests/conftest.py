"""Shared test fixtures for Phase 5 tests."""

import pytest
import sqlite3
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_database():
    """Fixture providing a temporary test database."""
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_restaurant.db")
    
    # Create database and table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cuisine TEXT,
            location TEXT,
            rating REAL,
            price REAL
        )
    """)
    
    # Insert test data
    test_restaurants = [
        (1, 'Pasta Paradise', 'italian', 'downtown', 4.5, 25.0),
        (2, 'Pizza Palace', 'italian', 'downtown', 4.3, 20.0),
        (3, 'Trattoria Roma', 'italian', 'downtown', 4.7, 35.0),
        (4, 'Bella Italia', 'italian', 'uptown', 4.2, 28.0),
        (5, 'Taco Heaven', 'mexican', 'downtown', 4.6, 15.0),
        (6, 'Burrito Palace', 'mexican', 'uptown', 4.4, 12.0),
        (7, 'Sushi Master', 'japanese', 'downtown', 4.8, 40.0),
        (8, 'Ramen House', 'japanese', 'downtown', 4.5, 18.0),
    ]
    
    cursor.executemany(
        "INSERT INTO restaurants VALUES (?, ?, ?, ?, ?, ?)",
        test_restaurants
    )
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup
    try:
        os.remove(db_path)
        os.rmdir(temp_dir)
    except:
        pass


@pytest.fixture
def sample_preferences():
    """Fixture providing sample user preferences."""
    return {
        'cuisine': 'italian',
        'location': 'downtown',
        'min_rating': 4.0,
        'max_price': 30.0,
        'limit': 3
    }


@pytest.fixture
def minimal_preferences():
    """Fixture providing minimal preferences."""
    return {
        'limit': 5
    }


@pytest.fixture
def invalid_preferences():
    """Fixture providing invalid preferences."""
    return {
        'cuisine': 123,  # Should be string
        'min_rating': 10.0  # Out of range
    }


@pytest.fixture
def sample_restaurants():
    """Fixture providing sample restaurant data."""
    return [
        {
            'id': 1,
            'name': 'Pasta Paradise',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.5,
            'price': 25.0
        },
        {
            'id': 2,
            'name': 'Pizza Palace',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.3,
            'price': 20.0
        },
        {
            'id': 3,
            'name': 'Trattoria Roma',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.7,
            'price': 35.0
        }
    ]


@pytest.fixture
def sample_llm_recommendations():
    """Fixture providing sample LLM recommendations."""
    return [
        {
            'name': 'Trattoria Roma',
            'explanation': 'Highest rated Italian restaurant in downtown with excellent reviews.'
        },
        {
            'name': 'Pasta Paradise',
            'explanation': 'Popular downtown Italian spot with authentic pasta dishes.'
        },
        {
            'name': 'Pizza Palace',
            'explanation': 'Great value Italian restaurant with good ratings.'
        }
    ]

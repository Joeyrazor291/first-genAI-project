"""Shared test fixtures for Phase 4 tests."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def sample_preferences():
    """Fixture providing sample user preferences."""
    return {
        'cuisine': 'italian',
        'location': 'downtown',
        'min_rating': 4.0,
        'max_price': 30.0,
        'limit': 5
    }


@pytest.fixture
def sample_restaurants():
    """Fixture providing sample restaurant data."""
    return [
        {
            'name': 'Pasta Paradise',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.5,
            'price': 25.0
        },
        {
            'name': 'Pizza Palace',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.3,
            'price': 20.0
        },
        {
            'name': 'Trattoria Roma',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.7,
            'price': 35.0
        },
        {
            'name': 'Bella Italia',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.2,
            'price': 28.0
        },
        {
            'name': 'La Cucina',
            'cuisine': 'italian',
            'location': 'downtown',
            'rating': 4.6,
            'price': 30.0
        }
    ]


@pytest.fixture
def mock_llm_response():
    """Fixture providing a mock LLM response."""
    return {
        'recommendations': [
            {
                'name': 'Trattoria Roma',
                'explanation': 'Highest rated Italian restaurant in downtown with excellent reviews.'
            },
            {
                'name': 'La Cucina',
                'explanation': 'Great Italian cuisine at your preferred price point with 4.6 stars.'
            },
            {
                'name': 'Pasta Paradise',
                'explanation': 'Popular downtown Italian spot with authentic pasta dishes.'
            }
        ]
    }


@pytest.fixture
def mock_groq_response(mock_llm_response):
    """Fixture providing a mock Groq API response."""
    import json
    
    # Create mock response object
    mock_response = Mock()
    mock_choice = Mock()
    mock_message = Mock()
    
    # Set up the mock chain
    mock_message.content = json.dumps(mock_llm_response)
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    return mock_response


@pytest.fixture
def minimal_preferences():
    """Fixture providing minimal user preferences."""
    return {
        'limit': 5
    }


@pytest.fixture
def empty_restaurants():
    """Fixture providing empty restaurant list."""
    return []


@pytest.fixture
def invalid_llm_response():
    """Fixture providing an invalid LLM response."""
    return "This is not valid JSON"


@pytest.fixture
def malformed_recommendations():
    """Fixture providing malformed recommendation data."""
    return {
        'recommendations': [
            {'name': 'Restaurant 1'},  # Missing explanation
            {'explanation': 'Good food'},  # Missing name
            {'name': 'Restaurant 3', 'explanation': 'Great place'}  # Valid
        ]
    }

"""Shared test fixtures for Phase 3 tests."""

import pytest


@pytest.fixture
def valid_preferences():
    """Fixture providing valid user preferences."""
    return {
        'cuisine': 'Italian',
        'location': 'Downtown',
        'min_rating': 4.0,
        'max_price': 30.0,
        'limit': 5
    }


@pytest.fixture
def minimal_preferences():
    """Fixture providing minimal user preferences."""
    return {}


@pytest.fixture
def preferences_with_invalid_rating():
    """Fixture providing preferences with invalid rating."""
    return {
        'cuisine': 'italian',
        'min_rating': 6.0  # Invalid: > 5.0
    }


@pytest.fixture
def preferences_with_invalid_price():
    """Fixture providing preferences with invalid price."""
    return {
        'cuisine': 'italian',
        'max_price': -10.0  # Invalid: negative
    }


@pytest.fixture
def preferences_with_invalid_limit():
    """Fixture providing preferences with invalid limit."""
    return {
        'cuisine': 'italian',
        'limit': 200  # Invalid: > 100
    }


@pytest.fixture
def preferences_with_empty_strings():
    """Fixture providing preferences with empty strings."""
    return {
        'cuisine': '   ',
        'location': ''
    }


@pytest.fixture
def preferences_with_wrong_types():
    """Fixture providing preferences with wrong data types."""
    return {
        'cuisine': 123,
        'min_rating': 'four',
        'max_price': 'expensive',
        'limit': 'ten'
    }


@pytest.fixture
def preferences_with_unknown_cuisine():
    """Fixture providing preferences with unknown cuisine."""
    return {
        'cuisine': 'martian',
        'min_rating': 4.0
    }

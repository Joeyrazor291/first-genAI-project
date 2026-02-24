"""Preference processor for validating and normalizing user inputs."""

import logging
from typing import Dict, Any, Optional
from src.models import UserPreferences
from src.config import (
    DEFAULT_MIN_RATING,
    DEFAULT_MAX_PRICE,
    DEFAULT_LIMIT,
    MIN_RATING_ALLOWED,
    MAX_RATING_ALLOWED,
    MIN_PRICE_ALLOWED,
    MAX_LIMIT
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PreferenceProcessor:
    """Processes and validates user preferences."""
    
    @staticmethod
    def validate_preferences(preferences: UserPreferences) -> Dict[str, Any]:
        """
        Validate and normalize user preferences.
        
        Args:
            preferences: User preferences from request.
            
        Returns:
            Dictionary of validated preferences with defaults applied.
            
        Raises:
            ValueError: If preferences are invalid.
        """
        validated = {}
        
        # Cuisine (optional, already normalized by Pydantic)
        if preferences.cuisine:
            validated['cuisine'] = preferences.cuisine
            logger.info(f"Cuisine filter: {preferences.cuisine}")
        
        # Location (optional, already normalized by Pydantic)
        if preferences.location:
            validated['location'] = preferences.location
            logger.info(f"Location filter: {preferences.location}")
        
        # Min Rating (optional, with default)
        if preferences.min_rating is not None:
            if not (MIN_RATING_ALLOWED <= preferences.min_rating <= MAX_RATING_ALLOWED):
                raise ValueError(
                    f"min_rating must be between {MIN_RATING_ALLOWED} and {MAX_RATING_ALLOWED}"
                )
            validated['min_rating'] = preferences.min_rating
            logger.info(f"Min rating filter: {preferences.min_rating}")
        
        # Max Price (optional, with default)
        if preferences.max_price is not None:
            if preferences.max_price < MIN_PRICE_ALLOWED:
                raise ValueError(f"max_price must be >= {MIN_PRICE_ALLOWED}")
            validated['max_price'] = preferences.max_price
            logger.info(f"Max price filter: {preferences.max_price}")
        
        # Limit (with default)
        limit = preferences.limit if preferences.limit is not None else DEFAULT_LIMIT
        if not (1 <= limit <= MAX_LIMIT):
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
        validated['limit'] = limit
        
        return validated
    
    @staticmethod
    def apply_defaults(preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply default values for missing preferences.
        
        Args:
            preferences: Validated preferences dictionary.
            
        Returns:
            Preferences with defaults applied.
        """
        defaults = {
            'min_rating': DEFAULT_MIN_RATING,
            'max_price': DEFAULT_MAX_PRICE,
            'limit': DEFAULT_LIMIT
        }
        
        # Apply defaults for missing keys
        for key, default_value in defaults.items():
            if key not in preferences:
                preferences[key] = default_value
        
        return preferences
    
    @staticmethod
    def get_filter_summary(preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of applied filters for response.
        
        Args:
            preferences: Validated preferences dictionary.
            
        Returns:
            Dictionary summarizing applied filters.
        """
        summary = {}
        
        if 'cuisine' in preferences:
            summary['cuisine'] = preferences['cuisine']
        
        if 'location' in preferences:
            summary['location'] = preferences['location']
        
        if 'min_rating' in preferences and preferences['min_rating'] > DEFAULT_MIN_RATING:
            summary['min_rating'] = preferences['min_rating']
        
        if 'max_price' in preferences and preferences['max_price'] < DEFAULT_MAX_PRICE:
            summary['max_price'] = preferences['max_price']
        
        if 'limit' in preferences:
            summary['limit'] = preferences['limit']
        
        return summary

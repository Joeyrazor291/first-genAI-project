"""Preference processor for validating and normalizing user inputs."""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of preference validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    normalized_preferences: Dict[str, Any] = field(default_factory=dict)


class PreferenceProcessor:
    """Processes and validates user preferences for restaurant recommendations."""
    
    # Validation constraints
    MIN_RATING = 0.0
    MAX_RATING = 5.0
    MIN_PRICE = 0.0
    MAX_PRICE = 10000.0
    MIN_LIMIT = 1
    MAX_LIMIT = 100
    DEFAULT_LIMIT = 10
    
    # Valid cuisine types (can be extended)
    VALID_CUISINES = {
        'italian', 'chinese', 'mexican', 'indian', 'japanese', 'thai',
        'french', 'american', 'mediterranean', 'korean', 'vietnamese',
        'greek', 'spanish', 'middle eastern', 'brazilian', 'caribbean'
    }
    
    def __init__(self):
        """Initialize preference processor."""
        logger.info("Preference processor initialized")
    
    def validate_and_normalize(
        self,
        preferences: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate and normalize user preferences.
        
        Args:
            preferences: Raw user preferences dictionary.
            
        Returns:
            ValidationResult with validation status and normalized preferences.
        """
        result = ValidationResult(is_valid=True)
        normalized = {}
        
        # Validate and normalize cuisine
        if 'cuisine' in preferences and preferences['cuisine'] is not None:
            cuisine_result = self._validate_cuisine(preferences['cuisine'])
            if cuisine_result['valid']:
                normalized['cuisine'] = cuisine_result['normalized']
            else:
                result.errors.append(cuisine_result['error'])
                result.is_valid = False
            
            if cuisine_result.get('warning'):
                result.warnings.append(cuisine_result['warning'])
        
        # Validate and normalize location
        if 'location' in preferences and preferences['location'] is not None:
            location_result = self._validate_location(preferences['location'])
            if location_result['valid']:
                normalized['location'] = location_result['normalized']
            else:
                result.errors.append(location_result['error'])
                result.is_valid = False
        
        # Validate and normalize min_rating
        if 'min_rating' in preferences and preferences['min_rating'] is not None:
            rating_result = self._validate_rating(preferences['min_rating'])
            if rating_result['valid']:
                normalized['min_rating'] = rating_result['normalized']
            else:
                result.errors.append(rating_result['error'])
                result.is_valid = False
        
        # Validate and normalize max_price
        if 'max_price' in preferences and preferences['max_price'] is not None:
            price_result = self._validate_price(preferences['max_price'])
            if price_result['valid']:
                normalized['max_price'] = price_result['normalized']
            else:
                result.errors.append(price_result['error'])
                result.is_valid = False
        
        # Validate and normalize limit
        if 'limit' in preferences and preferences['limit'] is not None:
            limit_result = self._validate_limit(preferences['limit'])
            if limit_result['valid']:
                normalized['limit'] = limit_result['normalized']
            else:
                result.errors.append(limit_result['error'])
                result.is_valid = False
        else:
            # Apply default limit
            normalized['limit'] = self.DEFAULT_LIMIT
        
        result.normalized_preferences = normalized
        
        if result.is_valid:
            logger.info(f"Preferences validated successfully: {normalized}")
        else:
            logger.warning(f"Preference validation failed: {result.errors}")
        
        return result
    
    def _validate_cuisine(self, cuisine: Any) -> Dict[str, Any]:
        """Validate and normalize cuisine preference."""
        if not isinstance(cuisine, str):
            return {
                'valid': False,
                'error': f"Cuisine must be a string, got {type(cuisine).__name__}"
            }
        
        # Normalize to lowercase and strip whitespace
        normalized = cuisine.strip().lower()
        
        if not normalized:
            return {
                'valid': False,
                'error': "Cuisine cannot be empty"
            }
        
        # Check if cuisine is in valid list (with warning if not)
        if normalized not in self.VALID_CUISINES:
            return {
                'valid': True,
                'normalized': normalized,
                'warning': f"Cuisine '{normalized}' is not in the standard list. Results may be limited."
            }
        
        return {
            'valid': True,
            'normalized': normalized
        }
    
    def _validate_location(self, location: Any) -> Dict[str, Any]:
        """Validate and normalize location preference."""
        if not isinstance(location, str):
            return {
                'valid': False,
                'error': f"Location must be a string, got {type(location).__name__}"
            }
        
        # Normalize to lowercase and strip whitespace
        normalized = location.strip().lower()
        
        if not normalized:
            return {
                'valid': False,
                'error': "Location cannot be empty"
            }
        
        return {
            'valid': True,
            'normalized': normalized
        }
    
    def _validate_rating(self, rating: Any) -> Dict[str, Any]:
        """Validate and normalize rating preference."""
        try:
            # Convert to float
            rating_float = float(rating)
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': f"Rating must be a number, got {type(rating).__name__}"
            }
        
        # Check range
        if rating_float < self.MIN_RATING or rating_float > self.MAX_RATING:
            return {
                'valid': False,
                'error': f"Rating must be between {self.MIN_RATING} and {self.MAX_RATING}, got {rating_float}"
            }
        
        return {
            'valid': True,
            'normalized': rating_float
        }
    
    def _validate_price(self, price: Any) -> Dict[str, Any]:
        """Validate and normalize price preference."""
        try:
            # Convert to float
            price_float = float(price)
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': f"Price must be a number, got {type(price).__name__}"
            }
        
        # Check range
        if price_float < self.MIN_PRICE:
            return {
                'valid': False,
                'error': f"Price must be >= {self.MIN_PRICE}, got {price_float}"
            }
        
        if price_float > self.MAX_PRICE:
            return {
                'valid': False,
                'error': f"Price must be <= {self.MAX_PRICE}, got {price_float}"
            }
        
        return {
            'valid': True,
            'normalized': price_float
        }
    
    def _validate_limit(self, limit: Any) -> Dict[str, Any]:
        """Validate and normalize limit preference."""
        try:
            # Convert to int
            limit_int = int(limit)
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': f"Limit must be an integer, got {type(limit).__name__}"
            }
        
        # Check range
        if limit_int < self.MIN_LIMIT or limit_int > self.MAX_LIMIT:
            return {
                'valid': False,
                'error': f"Limit must be between {self.MIN_LIMIT} and {self.MAX_LIMIT}, got {limit_int}"
            }
        
        return {
            'valid': True,
            'normalized': limit_int
        }
    
    def apply_defaults(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply default values for missing preferences.
        
        Args:
            preferences: Normalized preferences dictionary.
            
        Returns:
            Preferences with defaults applied.
        """
        defaults = {
            'limit': self.DEFAULT_LIMIT
        }
        
        # Apply defaults for missing keys
        for key, default_value in defaults.items():
            if key not in preferences:
                preferences[key] = default_value
                logger.debug(f"Applied default {key}={default_value}")
        
        return preferences
    
    def get_filter_summary(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of applied filters for response.
        
        Args:
            preferences: Normalized preferences dictionary.
            
        Returns:
            Dictionary summarizing applied filters.
        """
        summary = {}
        
        if 'cuisine' in preferences:
            summary['cuisine'] = preferences['cuisine']
        
        if 'location' in preferences:
            summary['location'] = preferences['location']
        
        if 'min_rating' in preferences:
            summary['min_rating'] = preferences['min_rating']
        
        if 'max_price' in preferences:
            summary['max_price'] = preferences['max_price']
        
        if 'limit' in preferences:
            summary['limit'] = preferences['limit']
        
        return summary

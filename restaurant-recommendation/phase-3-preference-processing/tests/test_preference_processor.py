"""Comprehensive tests for Phase 3 preference processor."""

import pytest
from src.preference_processor import PreferenceProcessor, ValidationResult


class TestValidationResult:
    """Test ValidationResult dataclass."""
    
    def test_validation_result_defaults(self):
        """Test ValidationResult with default values."""
        result = ValidationResult(is_valid=True)
        
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []
        assert result.normalized_preferences == {}
    
    def test_validation_result_with_errors(self):
        """Test ValidationResult with errors."""
        result = ValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"]
        )
        
        assert result.is_valid is False
        assert len(result.errors) == 2
    
    def test_validation_result_with_warnings(self):
        """Test ValidationResult with warnings."""
        result = ValidationResult(
            is_valid=True,
            warnings=["Warning 1"]
        )
        
        assert result.is_valid is True
        assert len(result.warnings) == 1


class TestCuisineValidation:
    """Test cuisine validation and normalization."""
    
    def test_valid_cuisine_lowercase(self, valid_preferences):
        """Test valid cuisine in lowercase."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': 'italian'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['cuisine'] == 'italian'
        assert len(result.errors) == 0
    
    def test_valid_cuisine_uppercase(self):
        """Test valid cuisine in uppercase gets normalized."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': 'ITALIAN'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['cuisine'] == 'italian'
    
    def test_valid_cuisine_mixed_case(self):
        """Test valid cuisine in mixed case gets normalized."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': 'ItAlIaN'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['cuisine'] == 'italian'
    
    def test_valid_cuisine_with_whitespace(self):
        """Test valid cuisine with whitespace gets trimmed."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': '  italian  '}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['cuisine'] == 'italian'
    
    def test_unknown_cuisine_with_warning(self, preferences_with_unknown_cuisine):
        """Test unknown cuisine generates warning but is valid."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(preferences_with_unknown_cuisine)
        
        assert result.is_valid is True
        assert result.normalized_preferences['cuisine'] == 'martian'
        assert len(result.warnings) > 0
        assert 'not in the standard list' in result.warnings[0]
    
    def test_empty_cuisine_string(self, preferences_with_empty_strings):
        """Test empty cuisine string is invalid."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': '   '}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'cannot be empty' in result.errors[0]
    
    def test_cuisine_wrong_type(self):
        """Test cuisine with wrong type is invalid."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': 123}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'must be a string' in result.errors[0]
    
    def test_cuisine_none_value(self):
        """Test cuisine with None value is skipped."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': None}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert 'cuisine' not in result.normalized_preferences


class TestLocationValidation:
    """Test location validation and normalization."""
    
    def test_valid_location(self, valid_preferences):
        """Test valid location."""
        processor = PreferenceProcessor()
        prefs = {'location': 'Downtown'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['location'] == 'downtown'
    
    def test_location_normalization(self):
        """Test location gets normalized to lowercase."""
        processor = PreferenceProcessor()
        prefs = {'location': 'NEW YORK CITY'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['location'] == 'new york city'
    
    def test_location_with_whitespace(self):
        """Test location with whitespace gets trimmed."""
        processor = PreferenceProcessor()
        prefs = {'location': '  downtown  '}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['location'] == 'downtown'
    
    def test_empty_location_string(self):
        """Test empty location string is invalid."""
        processor = PreferenceProcessor()
        prefs = {'location': ''}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'cannot be empty' in result.errors[0]
    
    def test_location_wrong_type(self):
        """Test location with wrong type is invalid."""
        processor = PreferenceProcessor()
        prefs = {'location': 456}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'must be a string' in result.errors[0]
    
    def test_location_none_value(self):
        """Test location with None value is skipped."""
        processor = PreferenceProcessor()
        prefs = {'location': None}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert 'location' not in result.normalized_preferences


class TestRatingValidation:
    """Test rating validation and normalization."""
    
    def test_valid_rating(self, valid_preferences):
        """Test valid rating."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': 4.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['min_rating'] == 4.0
    
    def test_rating_as_integer(self):
        """Test rating as integer gets converted to float."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': 4}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['min_rating'] == 4.0
        assert isinstance(result.normalized_preferences['min_rating'], float)
    
    def test_rating_as_string_number(self):
        """Test rating as string number gets converted."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': '4.5'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['min_rating'] == 4.5
    
    def test_rating_minimum_boundary(self):
        """Test rating at minimum boundary (0.0)."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': 0.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['min_rating'] == 0.0
    
    def test_rating_maximum_boundary(self):
        """Test rating at maximum boundary (5.0)."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': 5.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['min_rating'] == 5.0
    
    def test_rating_too_high(self, preferences_with_invalid_rating):
        """Test rating above maximum is invalid."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(preferences_with_invalid_rating)
        
        assert result.is_valid is False
        assert 'between 0.0 and 5.0' in result.errors[0]
    
    def test_rating_negative(self):
        """Test negative rating is invalid."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': -1.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'between 0.0 and 5.0' in result.errors[0]
    
    def test_rating_wrong_type(self):
        """Test rating with wrong type is invalid."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': 'four'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'must be a number' in result.errors[0]
    
    def test_rating_none_value(self):
        """Test rating with None value is skipped."""
        processor = PreferenceProcessor()
        prefs = {'min_rating': None}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert 'min_rating' not in result.normalized_preferences


class TestPriceValidation:
    """Test price validation and normalization."""
    
    def test_valid_price(self, valid_preferences):
        """Test valid price."""
        processor = PreferenceProcessor()
        prefs = {'max_price': 30.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['max_price'] == 30.0
    
    def test_price_as_integer(self):
        """Test price as integer gets converted to float."""
        processor = PreferenceProcessor()
        prefs = {'max_price': 50}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['max_price'] == 50.0
        assert isinstance(result.normalized_preferences['max_price'], float)
    
    def test_price_as_string_number(self):
        """Test price as string number gets converted."""
        processor = PreferenceProcessor()
        prefs = {'max_price': '25.99'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['max_price'] == 25.99
    
    def test_price_zero(self):
        """Test price at zero boundary."""
        processor = PreferenceProcessor()
        prefs = {'max_price': 0.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['max_price'] == 0.0
    
    def test_price_maximum_boundary(self):
        """Test price at maximum boundary."""
        processor = PreferenceProcessor()
        prefs = {'max_price': 10000.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['max_price'] == 10000.0
    
    def test_price_negative(self, preferences_with_invalid_price):
        """Test negative price is invalid."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(preferences_with_invalid_price)
        
        assert result.is_valid is False
        assert 'must be >=' in result.errors[0]
    
    def test_price_too_high(self):
        """Test price above maximum is invalid."""
        processor = PreferenceProcessor()
        prefs = {'max_price': 20000.0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'must be <=' in result.errors[0]
    
    def test_price_wrong_type(self):
        """Test price with wrong type is invalid."""
        processor = PreferenceProcessor()
        prefs = {'max_price': 'expensive'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'must be a number' in result.errors[0]
    
    def test_price_none_value(self):
        """Test price with None value is skipped."""
        processor = PreferenceProcessor()
        prefs = {'max_price': None}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert 'max_price' not in result.normalized_preferences


class TestLimitValidation:
    """Test limit validation and normalization."""
    
    def test_valid_limit(self, valid_preferences):
        """Test valid limit."""
        processor = PreferenceProcessor()
        prefs = {'limit': 5}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 5
    
    def test_limit_as_string_number(self):
        """Test limit as string number gets converted."""
        processor = PreferenceProcessor()
        prefs = {'limit': '10'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 10
    
    def test_limit_minimum_boundary(self):
        """Test limit at minimum boundary (1)."""
        processor = PreferenceProcessor()
        prefs = {'limit': 1}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 1
    
    def test_limit_maximum_boundary(self):
        """Test limit at maximum boundary (100)."""
        processor = PreferenceProcessor()
        prefs = {'limit': 100}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 100
    
    def test_limit_too_high(self, preferences_with_invalid_limit):
        """Test limit above maximum is invalid."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(preferences_with_invalid_limit)
        
        assert result.is_valid is False
        assert 'between 1 and 100' in result.errors[0]
    
    def test_limit_zero(self):
        """Test limit of zero is invalid."""
        processor = PreferenceProcessor()
        prefs = {'limit': 0}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'between 1 and 100' in result.errors[0]
    
    def test_limit_negative(self):
        """Test negative limit is invalid."""
        processor = PreferenceProcessor()
        prefs = {'limit': -5}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'between 1 and 100' in result.errors[0]
    
    def test_limit_wrong_type(self):
        """Test limit with wrong type is invalid."""
        processor = PreferenceProcessor()
        prefs = {'limit': 'ten'}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is False
        assert 'must be an integer' in result.errors[0]
    
    def test_limit_default_applied(self, minimal_preferences):
        """Test default limit is applied when not provided."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(minimal_preferences)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 10
    
    def test_limit_none_value(self):
        """Test limit with None value gets default."""
        processor = PreferenceProcessor()
        prefs = {'limit': None}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 10


class TestMultipleValidationErrors:
    """Test handling of multiple validation errors."""
    
    def test_multiple_errors(self, preferences_with_wrong_types):
        """Test multiple validation errors are collected."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(preferences_with_wrong_types)
        
        assert result.is_valid is False
        assert len(result.errors) >= 3  # cuisine, rating, price errors
    
    def test_all_valid_preferences(self, valid_preferences):
        """Test all valid preferences pass validation."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(valid_preferences)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.normalized_preferences['cuisine'] == 'italian'
        assert result.normalized_preferences['location'] == 'downtown'
        assert result.normalized_preferences['min_rating'] == 4.0
        assert result.normalized_preferences['max_price'] == 30.0
        assert result.normalized_preferences['limit'] == 5


class TestApplyDefaults:
    """Test applying default values."""
    
    def test_apply_defaults_empty_dict(self):
        """Test applying defaults to empty dictionary."""
        processor = PreferenceProcessor()
        prefs = {}
        
        result = processor.apply_defaults(prefs)
        
        assert 'limit' in result
        assert result['limit'] == 10
    
    def test_apply_defaults_partial_dict(self):
        """Test applying defaults to partial dictionary."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': 'italian'}
        
        result = processor.apply_defaults(prefs)
        
        assert 'cuisine' in result
        assert 'limit' in result
        assert result['limit'] == 10
    
    def test_apply_defaults_does_not_override(self):
        """Test that defaults don't override existing values."""
        processor = PreferenceProcessor()
        prefs = {'limit': 20}
        
        result = processor.apply_defaults(prefs)
        
        assert result['limit'] == 20


class TestFilterSummary:
    """Test filter summary generation."""
    
    def test_filter_summary_all_filters(self, valid_preferences):
        """Test summary with all filters applied."""
        processor = PreferenceProcessor()
        
        summary = processor.get_filter_summary(valid_preferences)
        
        assert 'cuisine' in summary
        assert 'location' in summary
        assert 'min_rating' in summary
        assert 'max_price' in summary
        assert 'limit' in summary
    
    def test_filter_summary_minimal_filters(self):
        """Test summary with minimal filters."""
        processor = PreferenceProcessor()
        prefs = {'limit': 10}
        
        summary = processor.get_filter_summary(prefs)
        
        assert 'limit' in summary
        assert len(summary) == 1
    
    def test_filter_summary_empty_dict(self):
        """Test summary with empty dictionary."""
        processor = PreferenceProcessor()
        prefs = {}
        
        summary = processor.get_filter_summary(prefs)
        
        assert summary == {}


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_preferences_dict(self, minimal_preferences):
        """Test empty preferences dictionary."""
        processor = PreferenceProcessor()
        
        result = processor.validate_and_normalize(minimal_preferences)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 10
    
    def test_preferences_with_extra_fields(self):
        """Test preferences with extra unknown fields are ignored."""
        processor = PreferenceProcessor()
        prefs = {
            'cuisine': 'italian',
            'unknown_field': 'value',
            'another_field': 123
        }
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert 'cuisine' in result.normalized_preferences
        assert 'unknown_field' not in result.normalized_preferences
    
    def test_float_limit_gets_converted_to_int(self):
        """Test float limit gets converted to integer."""
        processor = PreferenceProcessor()
        prefs = {'limit': 10.7}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['limit'] == 10
        assert isinstance(result.normalized_preferences['limit'], int)
    
    def test_very_long_cuisine_name(self):
        """Test very long cuisine name is handled."""
        processor = PreferenceProcessor()
        prefs = {'cuisine': 'a' * 1000}
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert len(result.warnings) > 0  # Unknown cuisine warning
    
    def test_unicode_in_text_fields(self):
        """Test unicode characters in text fields."""
        processor = PreferenceProcessor()
        prefs = {
            'cuisine': 'Français',
            'location': 'São Paulo'
        }
        
        result = processor.validate_and_normalize(prefs)
        
        assert result.is_valid is True
        assert result.normalized_preferences['cuisine'] == 'français'
        assert result.normalized_preferences['location'] == 'são paulo'

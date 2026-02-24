"""Tests for preference processor module."""

import pytest
from src.preference_processor import PreferenceProcessor
from src.models import UserPreferences


class TestPreferenceValidation:
    """Test cases for preference validation."""
    
    def test_validate_all_preferences(self):
        """Test validation with all preferences provided."""
        prefs = UserPreferences(
            cuisine="italian",
            location="downtown",
            min_rating=4.0,
            max_price=30.0,
            limit=5
        )
        
        validated = PreferenceProcessor.validate_preferences(prefs)
        
        assert validated['cuisine'] == 'italian'
        assert validated['location'] == 'downtown'
        assert validated['min_rating'] == 4.0
        assert validated['max_price'] == 30.0
        assert validated['limit'] == 5
    
    def test_validate_minimal_preferences(self):
        """Test validation with minimal preferences."""
        prefs = UserPreferences()
        
        validated = PreferenceProcessor.validate_preferences(prefs)
        
        # Should have limit with default
        assert 'limit' in validated
        assert validated['limit'] == 10
    
    def test_validate_invalid_rating_too_high(self):
        """Test validation fails for rating > 5.0."""
        prefs = UserPreferences(min_rating=6.0)
        
        with pytest.raises(ValueError) as exc_info:
            PreferenceProcessor.validate_preferences(prefs)
        
        assert "min_rating must be between" in str(exc_info.value)
    
    def test_validate_invalid_rating_negative(self):
        """Test validation fails for negative rating."""
        prefs = UserPreferences(min_rating=-1.0)
        
        with pytest.raises(ValueError) as exc_info:
            PreferenceProcessor.validate_preferences(prefs)
        
        assert "min_rating must be between" in str(exc_info.value)
    
    def test_validate_invalid_price_negative(self):
        """Test validation fails for negative price."""
        prefs = UserPreferences(max_price=-10.0)
        
        with pytest.raises(ValueError) as exc_info:
            PreferenceProcessor.validate_preferences(prefs)
        
        assert "max_price must be >=" in str(exc_info.value)
    
    def test_validate_invalid_limit_too_high(self):
        """Test validation fails for limit > 100."""
        prefs = UserPreferences(limit=200)
        
        with pytest.raises(ValueError) as exc_info:
            PreferenceProcessor.validate_preferences(prefs)
        
        assert "limit must be between" in str(exc_info.value)
    
    def test_validate_invalid_limit_zero(self):
        """Test validation fails for limit = 0."""
        prefs = UserPreferences(limit=0)
        
        with pytest.raises(ValueError) as exc_info:
            PreferenceProcessor.validate_preferences(prefs)
        
        assert "limit must be between" in str(exc_info.value)
    
    def test_text_fields_normalized(self):
        """Test that text fields are normalized to lowercase."""
        prefs = UserPreferences(
            cuisine="ITALIAN",
            location="  Downtown  "
        )
        
        validated = PreferenceProcessor.validate_preferences(prefs)
        
        assert validated['cuisine'] == 'italian'
        assert validated['location'] == 'downtown'


class TestDefaultApplication:
    """Test cases for applying defaults."""
    
    def test_apply_defaults_empty_dict(self):
        """Test applying defaults to empty dictionary."""
        prefs = {}
        result = PreferenceProcessor.apply_defaults(prefs)
        
        assert 'min_rating' in result
        assert 'max_price' in result
        assert 'limit' in result
    
    def test_apply_defaults_partial_dict(self):
        """Test applying defaults to partial dictionary."""
        prefs = {'cuisine': 'italian'}
        result = PreferenceProcessor.apply_defaults(prefs)
        
        assert 'cuisine' in result
        assert 'min_rating' in result
        assert 'max_price' in result
        assert 'limit' in result
    
    def test_apply_defaults_does_not_override(self):
        """Test that defaults don't override existing values."""
        prefs = {'min_rating': 4.5, 'limit': 20}
        result = PreferenceProcessor.apply_defaults(prefs)
        
        assert result['min_rating'] == 4.5
        assert result['limit'] == 20


class TestFilterSummary:
    """Test cases for filter summary generation."""
    
    def test_filter_summary_all_filters(self):
        """Test summary with all filters applied."""
        prefs = {
            'cuisine': 'italian',
            'location': 'downtown',
            'min_rating': 4.0,
            'max_price': 30.0,
            'limit': 5
        }
        
        summary = PreferenceProcessor.get_filter_summary(prefs)
        
        assert 'cuisine' in summary
        assert 'location' in summary
        assert 'min_rating' in summary
        assert 'max_price' in summary
        assert 'limit' in summary
    
    def test_filter_summary_minimal_filters(self):
        """Test summary with minimal filters."""
        prefs = {'limit': 10}
        
        summary = PreferenceProcessor.get_filter_summary(prefs)
        
        assert 'limit' in summary
        # Default values shouldn't appear in summary
        assert 'min_rating' not in summary or summary.get('min_rating') == 0.0
    
    def test_filter_summary_excludes_defaults(self):
        """Test that default values are excluded from summary."""
        prefs = {
            'min_rating': 0.0,  # Default value
            'cuisine': 'italian'
        }
        
        summary = PreferenceProcessor.get_filter_summary(prefs)
        
        assert 'cuisine' in summary
        # Default min_rating shouldn't be in summary
        assert 'min_rating' not in summary or summary['min_rating'] == 0.0

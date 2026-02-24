"""Tests for prompt builder module."""

import pytest
from src.prompt_builder import PromptBuilder


class TestPromptBuilder:
    """Test cases for prompt builder."""
    
    def test_initialization(self):
        """Test prompt builder initialization."""
        builder = PromptBuilder()
        assert builder is not None
        assert hasattr(builder, 'SYSTEM_PROMPT')
    
    def test_build_recommendation_prompt_with_all_preferences(
        self, sample_preferences, sample_restaurants
    ):
        """Test building prompt with all preferences."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            sample_preferences, sample_restaurants, limit=5
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert 'italian' in prompt.lower()
        assert 'downtown' in prompt.lower()
        assert '4.0' in prompt
        assert '30.0' in prompt
    
    def test_build_recommendation_prompt_includes_restaurants(
        self, sample_preferences, sample_restaurants
    ):
        """Test that prompt includes restaurant details."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            sample_preferences, sample_restaurants, limit=5
        )
        
        # Check that restaurant names are in prompt
        for restaurant in sample_restaurants:
            assert restaurant['name'] in prompt
    
    def test_build_recommendation_prompt_with_minimal_preferences(
        self, minimal_preferences, sample_restaurants
    ):
        """Test building prompt with minimal preferences."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            minimal_preferences, sample_restaurants, limit=5
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
    
    def test_build_recommendation_prompt_with_empty_restaurants(
        self, sample_preferences, empty_restaurants
    ):
        """Test building prompt with empty restaurant list."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            sample_preferences, empty_restaurants, limit=5
        )
        
        assert isinstance(prompt, str)
        assert 'No restaurants available' in prompt
    
    def test_build_recommendation_prompt_custom_limit(
        self, sample_preferences, sample_restaurants
    ):
        """Test building prompt with custom limit."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            sample_preferences, sample_restaurants, limit=3
        )
        
        assert 'top 3' in prompt
    
    def test_format_preferences_all_fields(self, sample_preferences):
        """Test formatting preferences with all fields."""
        builder = PromptBuilder()
        
        formatted = builder._format_preferences(sample_preferences)
        
        assert 'Cuisine: Italian' in formatted
        assert 'Location: Downtown' in formatted
        assert 'Minimum Rating: 4.0' in formatted
        assert 'Maximum Price: $30.0' in formatted
        assert 'Number of Results: 5' in formatted
    
    def test_format_preferences_partial_fields(self):
        """Test formatting preferences with partial fields."""
        builder = PromptBuilder()
        preferences = {'cuisine': 'italian', 'min_rating': 4.0}
        
        formatted = builder._format_preferences(preferences)
        
        assert 'Cuisine: Italian' in formatted
        assert 'Minimum Rating: 4.0' in formatted
        assert 'Location' not in formatted
    
    def test_format_preferences_empty(self):
        """Test formatting empty preferences."""
        builder = PromptBuilder()
        
        formatted = builder._format_preferences({})
        
        assert 'No specific preferences' in formatted
    
    def test_format_restaurants_with_data(self, sample_restaurants):
        """Test formatting restaurants with data."""
        builder = PromptBuilder()
        
        formatted = builder._format_restaurants(sample_restaurants)
        
        assert 'Pasta Paradise' in formatted
        assert 'Pizza Palace' in formatted
        assert 'italian' in formatted
        assert 'downtown' in formatted
        assert '4.5' in formatted
    
    def test_format_restaurants_empty(self, empty_restaurants):
        """Test formatting empty restaurant list."""
        builder = PromptBuilder()
        
        formatted = builder._format_restaurants(empty_restaurants)
        
        assert 'No restaurants available' in formatted
    
    def test_format_restaurants_numbering(self, sample_restaurants):
        """Test that restaurants are numbered in output."""
        builder = PromptBuilder()
        
        formatted = builder._format_restaurants(sample_restaurants)
        
        assert '1.' in formatted
        assert '2.' in formatted
        assert '3.' in formatted
    
    def test_format_restaurants_missing_fields(self):
        """Test formatting restaurants with missing fields."""
        builder = PromptBuilder()
        restaurants = [
            {'name': 'Test Restaurant'},  # Missing other fields
            {}  # All fields missing
        ]
        
        formatted = builder._format_restaurants(restaurants)
        
        assert 'Test Restaurant' in formatted
        assert 'Unknown' in formatted
        assert 'N/A' in formatted
    
    def test_build_fallback_prompt(self, sample_preferences):
        """Test building fallback prompt."""
        builder = PromptBuilder()
        error_msg = "API timeout"
        
        prompt = builder.build_fallback_prompt(sample_preferences, error_msg)
        
        assert isinstance(prompt, str)
        assert error_msg in prompt
        assert 'italian' in prompt.lower()
    
    def test_build_fallback_prompt_with_minimal_preferences(
        self, minimal_preferences
    ):
        """Test building fallback prompt with minimal preferences."""
        builder = PromptBuilder()
        
        prompt = builder.build_fallback_prompt(minimal_preferences, "Error")
        
        assert isinstance(prompt, str)
        assert 'Error' in prompt
    
    def test_prompt_includes_json_format_instruction(
        self, sample_preferences, sample_restaurants
    ):
        """Test that prompt includes JSON format instruction."""
        builder = PromptBuilder()
        
        prompt = builder.build_recommendation_prompt(
            sample_preferences, sample_restaurants, limit=5
        )
        
        assert 'JSON' in prompt
        assert 'name' in prompt
        assert 'explanation' in prompt
    
    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        builder = PromptBuilder()
        
        assert hasattr(builder, 'SYSTEM_PROMPT')
        assert isinstance(builder.SYSTEM_PROMPT, str)
        assert len(builder.SYSTEM_PROMPT) > 0
        assert 'restaurant' in builder.SYSTEM_PROMPT.lower()

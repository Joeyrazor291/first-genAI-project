"""Prompt builder for LLM recommendation generation."""

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds prompts for LLM-based restaurant recommendations."""
    
    SYSTEM_PROMPT = """You are an expert restaurant recommendation assistant. Your task is to analyze user preferences and a list of restaurants, then provide personalized recommendations with clear explanations.

Guidelines:
- Recommend restaurants that best match the user's stated preferences
- Provide a brief, compelling explanation for each recommendation
- Consider all preference factors: cuisine, location, rating, and price
- Be concise but informative
- Format your response as a JSON array of recommendations
- CRITICAL: Each restaurant in your recommendations must be unique. Do not recommend the same restaurant more than once. Never repeat a restaurant name."""
    
    def __init__(self):
        """Initialize prompt builder."""
        logger.info("Prompt builder initialized")
    
    def build_recommendation_prompt(
        self,
        preferences: Dict[str, Any],
        restaurants: List[Dict[str, Any]],
        limit: int = 5
    ) -> str:
        """
        Build a prompt for restaurant recommendations.
        
        Args:
            preferences: User preferences dictionary
            restaurants: List of restaurant dictionaries
            limit: Number of recommendations to generate
            
        Returns:
            Formatted prompt string
        """
        # Format user preferences
        prefs_text = self._format_preferences(preferences)
        
        # Format restaurant list
        restaurants_text = self._format_restaurants(restaurants)
        
        # Build the complete prompt
        prompt = f"""User Preferences:
{prefs_text}

Available Restaurants:
{restaurants_text}

Task: Based on the user's preferences, recommend the top {limit} restaurants from the list above. For each recommendation, provide:
1. Restaurant name
2. A brief explanation (1-2 sentences) of why it matches the user's preferences

Format your response as a JSON array with this structure:
[
  {{
    "name": "Restaurant Name",
    "explanation": "Why this restaurant is recommended"
  }}
]

Provide ONLY the JSON array, no additional text."""
        
        logger.debug(f"Built prompt with {len(restaurants)} restaurants")
        return prompt
    
    def _format_preferences(self, preferences: Dict[str, Any]) -> str:
        """Format user preferences for the prompt."""
        lines = []
        
        if 'cuisine' in preferences:
            lines.append(f"- Cuisine: {preferences['cuisine'].title()}")
        
        if 'location' in preferences:
            lines.append(f"- Location: {preferences['location'].title()}")
        
        if 'min_rating' in preferences:
            lines.append(f"- Minimum Rating: {preferences['min_rating']}/5.0")
        
        if 'max_price' in preferences:
            lines.append(f"- Maximum Price: ${preferences['max_price']}")
        
        if 'limit' in preferences:
            lines.append(f"- Number of Results: {preferences['limit']}")
        
        return "\n".join(lines) if lines else "- No specific preferences"
    
    def _format_restaurants(self, restaurants: List[Dict[str, Any]]) -> str:
        """Format restaurant list for the prompt."""
        if not restaurants:
            return "No restaurants available"
        
        lines = []
        for i, restaurant in enumerate(restaurants, 1):
            name = restaurant.get('name', 'Unknown')
            cuisine = restaurant.get('cuisine', 'N/A')
            location = restaurant.get('location', 'N/A')
            rating = restaurant.get('rating', 'N/A')
            price = restaurant.get('price', 'N/A')
            
            lines.append(
                f"{i}. {name}\n"
                f"   - Cuisine: {cuisine}\n"
                f"   - Location: {location}\n"
                f"   - Rating: {rating}/5.0\n"
                f"   - Price: ${price}"
            )
        
        return "\n\n".join(lines)
    
    def build_fallback_prompt(
        self,
        preferences: Dict[str, Any],
        error_message: str
    ) -> str:
        """
        Build a prompt for fallback recommendations when LLM fails.
        
        Args:
            preferences: User preferences dictionary
            error_message: Error message from failed LLM call
            
        Returns:
            Fallback prompt string
        """
        prefs_text = self._format_preferences(preferences)
        
        prompt = f"""The primary recommendation system encountered an error: {error_message}

User Preferences:
{prefs_text}

Please provide general restaurant recommendations based on these preferences. Keep recommendations generic but helpful."""
        
        logger.warning("Built fallback prompt due to error")
        return prompt

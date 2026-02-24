#!/usr/bin/env python3
"""Test script for OpenRouter LLM provider."""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import LLMConfig
from llm_service import LLMService
from prompt_builder import PromptBuilder


def test_openrouter():
    """Test OpenRouter LLM provider with demo input."""
    
    print("=" * 80)
    print("OpenRouter LLM Provider Test")
    print("=" * 80)
    
    try:
        # Load configuration
        print("\n1. Loading configuration...")
        config = LLMConfig.from_env()
        print(f"   ✓ Provider: {config.api_provider}")
        print(f"   ✓ Model: {config.model}")
        print(f"   ✓ Temperature: {config.temperature}")
        print(f"   ✓ Max tokens: {config.max_tokens}")
        
        # Initialize LLM service
        print("\n2. Initializing LLM service...")
        llm_service = LLMService(config)
        print("   ✓ LLM service initialized successfully")
        
        # Demo preferences
        demo_preferences = {
            "cuisine": "Italian",
            "location": "downtown",
            "min_rating": 4.0,
            "max_price": 50,
            "limit": 3
        }
        
        # Demo restaurants
        demo_restaurants = [
            {
                "name": "Bella Italia",
                "cuisine": "Italian",
                "location": "downtown",
                "rating": 4.8,
                "price": 45
            },
            {
                "name": "Pasta Paradise",
                "cuisine": "Italian",
                "location": "downtown",
                "rating": 4.6,
                "price": 35
            },
            {
                "name": "Roman Kitchen",
                "cuisine": "Italian",
                "location": "midtown",
                "rating": 4.5,
                "price": 40
            },
            {
                "name": "Trattoria Napoli",
                "cuisine": "Italian",
                "location": "downtown",
                "rating": 4.7,
                "price": 48
            },
            {
                "name": "Ristorante Venezia",
                "cuisine": "Italian",
                "location": "uptown",
                "rating": 4.4,
                "price": 55
            }
        ]
        
        print("\n3. Demo Input:")
        print(f"   Preferences: {json.dumps(demo_preferences, indent=2)}")
        print(f"   Number of restaurants: {len(demo_restaurants)}")
        
        # Generate recommendations
        print("\n4. Generating recommendations from OpenRouter...")
        print("   (This may take a few seconds...)")
        
        recommendations = llm_service.generate_recommendations(
            preferences=demo_preferences,
            restaurants=demo_restaurants,
            limit=3
        )
        
        print("\n5. OpenRouter Response:")
        print(f"   ✓ Successfully generated {len(recommendations)} recommendations")
        print("\n   Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n   {i}. {rec['name']}")
            print(f"      Explanation: {rec['explanation']}")
        
        # Test health check
        print("\n6. Health Check:")
        health = llm_service.health_check()
        print(f"   ✓ Status: {health['status']}")
        print(f"   ✓ Model: {health['model']}")
        print(f"   ✓ API Accessible: {health['api_accessible']}")
        
        print("\n" + "=" * 80)
        print("✓ OpenRouter LLM Provider Test PASSED")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\n" + "=" * 80)
        print("✗ OpenRouter LLM Provider Test FAILED")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_openrouter()
    sys.exit(0 if success else 1)

"""Verification script to test Phase 4 LLM Integration setup."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.llm_service import LLMService, LLMServiceError


def main():
    """Run verification tests."""
    print("=" * 60)
    print("Phase 4 LLM Integration - Setup Verification")
    print("=" * 60)
    
    # Test 1: Initialize service
    print("\n[1/4] Initializing LLM service...")
    try:
        service = LLMService()
        print("✅ Service initialized successfully")
        print(f"   Model: {service.config.model}")
        print(f"   Temperature: {service.config.temperature}")
        print(f"   Max Tokens: {service.config.max_tokens}")
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        return False
    
    # Test 2: Health check
    print("\n[2/4] Running health check...")
    try:
        health = service.health_check()
        if health['status'] == 'healthy':
            print("✅ Health check passed")
            print(f"   Status: {health['status']}")
            print(f"   Model: {health['model']}")
            print(f"   API Accessible: {health['api_accessible']}")
        else:
            print(f"❌ Health check failed: {health.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 3: Generate test recommendations
    print("\n[3/4] Testing recommendation generation...")
    
    preferences = {
        'cuisine': 'italian',
        'location': 'downtown',
        'min_rating': 4.0,
        'max_price': 30.0
    }
    
    restaurants = [
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
        }
    ]
    
    try:
        recommendations = service.generate_recommendations(
            preferences=preferences,
            restaurants=restaurants,
            limit=2
        )
        
        if recommendations and len(recommendations) > 0:
            print("✅ Recommendations generated successfully")
            print(f"   Generated {len(recommendations)} recommendations")
            for i, rec in enumerate(recommendations, 1):
                print(f"\n   {i}. {rec['name']}")
                print(f"      {rec['explanation'][:80]}...")
        else:
            print("⚠️  No recommendations generated (empty response)")
            return False
            
    except LLMServiceError as e:
        print(f"❌ Failed to generate recommendations: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test 4: Test fallback recommendations
    print("\n[4/4] Testing fallback recommendations...")
    try:
        fallback_recs = service.generate_fallback_recommendations(
            restaurants=restaurants,
            limit=2
        )
        
        if fallback_recs and len(fallback_recs) > 0:
            print("✅ Fallback recommendations working")
            print(f"   Generated {len(fallback_recs)} fallback recommendations")
        else:
            print("⚠️  Fallback recommendations returned empty")
            
    except Exception as e:
        print(f"❌ Fallback error: {e}")
        return False
    
    # All tests passed
    print("\n" + "=" * 60)
    print("✅ ALL VERIFICATION TESTS PASSED!")
    print("=" * 60)
    print("\nPhase 4 is ready to use. You can now:")
    print("  1. Run integration tests: pytest tests/test_integration.py -v")
    print("  2. Integrate with other phases")
    print("  3. Start building Phase 5 (Recommendation Engine)")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""Test script for OpenRouter API integration."""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from Phase 4
phase4_env = Path("restaurant-recommendation/phase-4-llm-integration/.env")
if phase4_env.exists():
    load_dotenv(phase4_env)
    print(f"✓ Loaded .env from {phase4_env}")
else:
    print(f"✗ .env file not found at {phase4_env}")

# Add Phase 4 to path
sys.path.insert(0, str(Path("restaurant-recommendation/phase-4-llm-integration/src")))

print("\n" + "="*60)
print("OPENROUTER API INTEGRATION TEST")
print("="*60)

# Test 1: Check environment variables
print("\n[TEST 1] Checking environment variables...")
provider = os.getenv("LLM_PROVIDER", "not set")
openrouter_key = os.getenv("OPENROUTER_API_KEY", "not set")
openrouter_model = os.getenv("OPENROUTER_MODEL", "not set")

print(f"  LLM_PROVIDER: {provider}")
print(f"  OPENROUTER_API_KEY: {'***' + openrouter_key[-10:] if openrouter_key != 'not set' else 'NOT SET'}")
print(f"  OPENROUTER_MODEL: {openrouter_model}")

if provider != "openrouter":
    print(f"  ✗ ERROR: LLM_PROVIDER is '{provider}', expected 'openrouter'")
    sys.exit(1)

if openrouter_key == "not set":
    print(f"  ✗ ERROR: OPENROUTER_API_KEY not set")
    sys.exit(1)

print("  ✓ Environment variables OK")

# Test 2: Load LLM Config
print("\n[TEST 2] Loading LLM configuration...")
try:
    from config import LLMConfig
    config = LLMConfig.from_env()
    print(f"  API Provider: {config.api_provider}")
    print(f"  Model: {config.model}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    print(f"  Max Retries: {config.max_retries}")
    print("  ✓ Configuration loaded successfully")
except Exception as e:
    print(f"  ✗ ERROR: Failed to load configuration: {e}")
    sys.exit(1)

# Test 3: Initialize LLM Service
print("\n[TEST 3] Initializing LLM Service...")
try:
    from llm_service import LLMService
    llm_service = LLMService(config=config)
    print(f"  ✓ LLM Service initialized")
except Exception as e:
    print(f"  ✗ ERROR: Failed to initialize LLM service: {e}")
    sys.exit(1)

# Test 4: Health Check
print("\n[TEST 4] Running health check...")
try:
    health = llm_service.health_check()
    print(f"  Status: {health.get('status')}")
    print(f"  Model: {health.get('model')}")
    print(f"  API Accessible: {health.get('api_accessible')}")
    
    if health.get('status') == 'healthy':
        print("  ✓ Health check PASSED")
    else:
        error = health.get('error', 'Unknown error')
        print(f"  ✗ Health check FAILED: {error}")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ ERROR: Health check failed: {e}")
    sys.exit(1)

# Test 5: Simple API Call
print("\n[TEST 5] Testing simple API call...")
try:
    test_prompt = "Recommend 2 Italian restaurants with brief explanations in JSON format: [{\"name\": \"...\", \"explanation\": \"...\"}]"
    response = llm_service._call_llm(test_prompt)
    print(f"  Response received from OpenRouter")
    print(f"  Model used: {response.model}")
    print(f"  Tokens used: {response.usage.total_tokens}")
    print("  ✓ API call successful")
except Exception as e:
    print(f"  ✗ ERROR: API call failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Full Recommendation Generation
print("\n[TEST 6] Testing full recommendation generation...")
try:
    test_restaurants = [
        {"name": "Pizza Palace", "cuisine": "Italian", "location": "Downtown", "rating": 4.5, "price": 300},
        {"name": "Pasta House", "cuisine": "Italian", "location": "Midtown", "rating": 4.2, "price": 250},
        {"name": "Trattoria Roma", "cuisine": "Italian", "location": "Uptown", "rating": 4.8, "price": 400},
    ]
    
    test_preferences = {
        "cuisine": "Italian",
        "min_rating": 4.0,
        "location": "Downtown"
    }
    
    recommendations = llm_service.generate_recommendations(
        preferences=test_preferences,
        restaurants=test_restaurants,
        limit=2
    )
    
    print(f"  Generated {len(recommendations)} recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"    {i}. {rec['name']}")
        print(f"       {rec['explanation'][:100]}...")
    
    if len(recommendations) > 0:
        print("  ✓ Recommendation generation successful")
    else:
        print("  ✗ No recommendations generated")
        sys.exit(1)
        
except Exception as e:
    print(f"  ✗ ERROR: Recommendation generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✓ ALL TESTS PASSED - OpenRouter API is working!")
print("="*60)

# Phase 4 Setup Guide

## Quick Start

### Step 1: Install Dependencies

```bash
cd restaurant-recommendation/phase-4-llm-integration
pip install -r requirements.txt
```

### Step 2: Get Groq API Key

1. Visit https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again!)

### Step 3: Configure Environment

1. Copy the example environment file:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Open `.env` in a text editor

3. Replace `your_groq_api_key_here` with your actual API key:
```env
GROQ_API_KEY=gsk_your_actual_key_here
```

4. Save the file

### Step 4: Verify Setup

Run this Python script to verify your setup:

```python
from src.llm_service import LLMService

# Initialize service
service = LLMService()

# Run health check
health = service.health_check()
print(f"Status: {health['status']}")
print(f"Model: {health['model']}")
print(f"API Accessible: {health['api_accessible']}")

if health['status'] == 'healthy':
    print("\n✅ Setup successful! LLM service is ready.")
else:
    print(f"\n❌ Setup failed: {health.get('error')}")
```

Save as `verify_setup.py` and run:
```bash
python verify_setup.py
```

Expected output:
```
Status: healthy
Model: llama-3.3-70b-versatile
API Accessible: True

✅ Setup successful! LLM service is ready.
```

### Step 5: Test Recommendations

Try generating a recommendation:

```python
from src.llm_service import LLMService

service = LLMService()

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
    }
]

try:
    recommendations = service.generate_recommendations(
        preferences=preferences,
        restaurants=restaurants,
        limit=2
    )
    
    print("\n✅ Recommendations generated successfully!")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['name']}")
        print(f"   {rec['explanation']}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
```

## Troubleshooting

### Error: "GROQ_API_KEY environment variable is required"

**Solution**: Make sure you created the `.env` file and added your API key.

### Error: "Authentication failed"

**Solution**: Your API key is invalid. Double-check you copied it correctly from Groq console.

### Error: "Rate limit exceeded"

**Solution**: You've hit the API rate limit. Wait a minute and try again, or upgrade your Groq plan.

### Error: "Module not found: groq"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Tests fail with API errors

**Solution**: For unit tests, you don't need an API key (they use mocks). For integration tests, make sure your API key is in `.env`.

## Running Tests

### Unit Tests (No API Key Required)
```bash
pytest tests/ -v
```

### Integration Tests (API Key Required)
```bash
pytest tests/ -v -m integration
```

### Specific Test File
```bash
pytest tests/test_llm_service.py -v
```

## Configuration Options

Edit `.env` to customize:

```env
# Required
GROQ_API_KEY=your_key_here

# Optional (defaults shown)
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024
MAX_RETRIES=3
RETRY_DELAY=1.0
```

### Available Models

- `llama-3.3-70b-versatile` (default) - Best for general tasks
- `llama-3.1-70b-versatile` - Alternative large model
- `mixtral-8x7b-32768` - Good for longer contexts
- `gemma2-9b-it` - Faster, smaller model

## Next Steps

Once setup is complete:

1. ✅ Phase 4 is ready to use
2. Integrate with Phase 3 (Preference Processing)
3. Integrate with Phase 5 (Recommendation Engine)
4. Monitor API usage and costs
5. Implement caching if needed

## Support

- Groq Documentation: https://console.groq.com/docs
- Groq API Status: https://status.groq.com
- Project README: See README.md in this directory

## Security Reminder

⚠️ **Never commit your `.env` file to version control!**

The `.gitignore` file already excludes it, but double-check:
```bash
git status
```

If you see `.env` listed, do NOT commit it. Your API key should remain private.

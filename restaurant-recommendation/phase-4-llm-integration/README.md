# Phase 4: LLM Integration

## Overview

Phase 4 implements the LLM integration layer for the AI Restaurant Recommendation Service using Groq API. This module generates intelligent, personalized restaurant recommendations by leveraging large language models to analyze user preferences and restaurant data.

## Purpose

The LLM integration module provides:
- Intelligent recommendation generation using Groq's LLM API
- Sophisticated prompt engineering for optimal results
- Retry logic with exponential backoff for reliability
- Fallback recommendations when LLM is unavailable
- Health monitoring for the LLM service

## Architecture Position

This phase sits between the recommendation engine and provides the intelligence layer:

```
Preferences (Phase 3) → Filtered Restaurants → LLM Integration (Phase 4) → Intelligent Recommendations → API Response
```

## Components

### LLMService

Main service class that handles LLM API communication and recommendation generation.

**Key Features**:
- Groq API integration with configurable models
- Automatic retry with exponential backoff
- Response parsing and validation
- Fallback recommendations (rule-based)
- Health check endpoint

### PromptBuilder

Constructs optimized prompts for the LLM based on user preferences and restaurant data.

**Key Features**:
- Structured prompt templates
- Preference formatting
- Restaurant data formatting
- JSON response format enforcement
- Fallback prompt generation

### LLMConfig

Configuration management for LLM service.

**Key Features**:
- Environment variable loading
- Configuration validation
- Default value management
- Type safety with dataclasses

## Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (get one at https://console.groq.com)
- pip package manager

### Setup

1. Navigate to the phase directory:
```bash
cd restaurant-recommendation/phase-4-llm-integration
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from template:
```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac
```

4. Add your Groq API key to `.env`:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (with defaults)
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024
MAX_RETRIES=3
RETRY_DELAY=1.0
```

### Available Models

Groq supports several models:
- `llama-3.3-70b-versatile` (default) - Best for general tasks
- `llama-3.1-70b-versatile` - Alternative large model
- `mixtral-8x7b-32768` - Good for longer contexts
- `gemma2-9b-it` - Faster, smaller model

## Usage

### Basic Usage

```python
from src.llm_service import LLMService
from src.config import LLMConfig

# Initialize service (loads config from .env)
service = LLMService()

# Or with custom config
config = LLMConfig(
    api_key="your_key",
    model="llama-3.3-70b-versatile",
    temperature=0.7
)
service = LLMService(config=config)

# Generate recommendations
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
    # ... more restaurants
]

recommendations = service.generate_recommendations(
    preferences=preferences,
    restaurants=restaurants,
    limit=5
)

# Output:
# [
#   {
#     'name': 'Pasta Paradise',
#     'explanation': 'Highly rated Italian restaurant in downtown...'
#   },
#   ...
# ]
```

### Error Handling

```python
from src.llm_service import LLMService, LLMServiceError

service = LLMService()

try:
    recommendations = service.generate_recommendations(
        preferences, restaurants, limit=5
    )
except LLMServiceError as e:
    print(f"LLM service error: {e}")
    # Use fallback recommendations
    recommendations = service.generate_fallback_recommendations(
        restaurants, limit=5
    )
```

### Fallback Recommendations

When the LLM is unavailable, use rule-based fallback:

```python
# Fallback recommendations (sorted by rating)
fallback_recs = service.generate_fallback_recommendations(
    restaurants=restaurants,
    limit=5
)
```

### Health Check

Monitor LLM service health:

```python
health_status = service.health_check()

if health_status['status'] == 'healthy':
    print("LLM service is operational")
else:
    print(f"LLM service issue: {health_status.get('error')}")
```

### Custom Prompts

Use the PromptBuilder directly for custom prompts:

```python
from src.prompt_builder import PromptBuilder

builder = PromptBuilder()

# Build recommendation prompt
prompt = builder.build_recommendation_prompt(
    preferences=preferences,
    restaurants=restaurants,
    limit=5
)

# Build fallback prompt
fallback_prompt = builder.build_fallback_prompt(
    preferences=preferences,
    error_message="API timeout"
)
```

## Testing

### Run All Tests (Mocked)

Tests use mocked API calls and don't require an API key:

```bash
pytest tests/ -v
```

### Run Specific Test Files

```bash
# Test configuration
pytest tests/test_config.py -v

# Test prompt builder
pytest tests/test_prompt_builder.py -v

# Test LLM service
pytest tests/test_llm_service.py -v
```

### Run Integration Tests (Requires API Key)

Integration tests make real API calls and require a valid Groq API key in `.env`:

```bash
pytest tests/ -v -m integration
```

**Note**: Integration tests are not included in the default test suite to avoid API costs during development.

### Test Coverage

The test suite includes 60+ comprehensive tests covering:
- ✅ Configuration management and validation
- ✅ Prompt building with various inputs
- ✅ LLM service initialization
- ✅ Recommendation generation (mocked)
- ✅ Retry logic and error handling
- ✅ Response parsing and validation
- ✅ Fallback recommendations
- ✅ Health check functionality
- ✅ Edge cases and error conditions

All tests pass successfully with mocked API calls.

## Project Structure

```
phase-4-llm-integration/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── prompt_builder.py      # Prompt engineering
│   └── llm_service.py         # Main LLM service
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_config.py         # Config tests
│   ├── test_prompt_builder.py # Prompt builder tests
│   └── test_llm_service.py    # LLM service tests
├── conftest.py                # Root pytest configuration
├── pytest.ini                 # Pytest settings
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Dependencies

```
groq>=0.4.0                    # Groq API client
python-dotenv>=1.0.0           # Environment variable management
pytest>=7.0.0                  # Testing framework
pytest-asyncio>=0.21.0         # Async test support
pytest-mock>=3.12.0            # Mocking utilities
```

## Integration with Other Phases

### Phase 3 (Preference Processing)
Phase 4 receives validated and normalized preferences from Phase 3.

### Phase 5 (Recommendation Engine)
Phase 5 orchestrates the flow: filters restaurants, calls Phase 4 for LLM recommendations, and formats the final response.

### Example Integration

```python
# In Phase 5 Recommendation Engine
from phase_3_preference_processing.src.preference_processor import PreferenceProcessor
from phase_4_llm_integration.src.llm_service import LLMService

# Validate preferences
processor = PreferenceProcessor()
result = processor.validate_and_normalize(user_input)

if not result.is_valid:
    return {"error": result.errors}

# Filter restaurants (from database)
filtered_restaurants = filter_restaurants(result.normalized_preferences)

# Generate LLM recommendations
llm_service = LLMService()
try:
    recommendations = llm_service.generate_recommendations(
        preferences=result.normalized_preferences,
        restaurants=filtered_restaurants,
        limit=5
    )
except LLMServiceError:
    # Use fallback
    recommendations = llm_service.generate_fallback_recommendations(
        restaurants=filtered_restaurants,
        limit=5
    )

return {"recommendations": recommendations}
```

## Performance Considerations

### Response Time
- Typical LLM response: 1-3 seconds
- With retry (3 attempts): up to 10 seconds
- Fallback response: < 100ms

### Rate Limiting
Groq API has rate limits:
- Free tier: 30 requests/minute
- Paid tier: Higher limits available

Implement rate limiting in your application layer.

### Caching
Consider caching LLM responses for identical queries:
```python
# Pseudo-code
cache_key = hash(preferences + restaurant_ids)
if cache_key in cache:
    return cache[cache_key]
else:
    recommendations = llm_service.generate_recommendations(...)
    cache[cache_key] = recommendations
    return recommendations
```

## Error Handling

### Common Errors

1. **Missing API Key**
```
ValueError: GROQ_API_KEY environment variable is required
```
Solution: Add API key to `.env` file

2. **Invalid API Key**
```
LLMServiceError: Failed to generate recommendations: Authentication failed
```
Solution: Verify API key is correct

3. **Rate Limit Exceeded**
```
LLMServiceError: Failed to generate recommendations: Rate limit exceeded
```
Solution: Implement rate limiting or upgrade API plan

4. **Network Timeout**
```
LLMServiceError: Failed to generate recommendations: Request timeout
```
Solution: Retry logic handles this automatically

### Retry Strategy

The service implements exponential backoff:
- Attempt 1: Immediate
- Attempt 2: Wait 1 second
- Attempt 3: Wait 2 seconds
- Attempt 4: Wait 4 seconds (if max_retries=4)

## Security Considerations

### API Key Protection
- Never commit `.env` file to version control
- Use environment variables in production
- Rotate API keys regularly
- Use separate keys for dev/staging/prod

### Input Validation
- Validate all inputs before sending to LLM
- Sanitize restaurant data to prevent prompt injection
- Limit prompt size to prevent abuse

### Output Validation
- Parse and validate LLM responses
- Handle malformed responses gracefully
- Log suspicious outputs for review

## Monitoring

### Key Metrics to Track
- LLM API response time
- Success rate (successful vs failed calls)
- Fallback usage rate
- Token usage (for cost tracking)
- Error types and frequencies

### Logging

The service logs important events:
```python
import logging
logging.basicConfig(level=logging.INFO)

# Logs include:
# - Service initialization
# - API calls and responses
# - Retry attempts
# - Errors and warnings
# - Fallback usage
```

## Future Enhancements

Potential improvements for future iterations:
- Support for multiple LLM providers (OpenAI, Anthropic, etc.)
- Streaming responses for real-time updates
- Fine-tuned models for restaurant recommendations
- A/B testing different prompts
- Response caching layer
- Advanced prompt templates
- Multi-language support
- Conversation history for follow-up questions

## Troubleshooting

### Tests Fail with "Module not found"
```bash
pip install -r requirements.txt
```

### Tests Fail with "API Key Required"
For mocked tests, this shouldn't happen. For integration tests, add API key to `.env`.

### LLM Returns Unexpected Format
Check the prompt template and ensure JSON format is enforced. The service validates responses and skips malformed recommendations.

### Slow Response Times
- Check network connectivity
- Verify Groq API status
- Consider using a faster model
- Implement caching

## Success Criteria

✅ LLM successfully generates recommendations  
✅ Retry logic handles transient failures  
✅ Fallback provides reasonable recommendations  
✅ Configuration management working  
✅ Prompt engineering optimized  
✅ 60+ comprehensive tests - all passing  
✅ Complete documentation  
✅ Error handling robust  

## Next Steps

After Phase 4, proceed to:
- **Phase 5**: Recommendation Engine - Orchestrate the complete recommendation pipeline
- **Phase 6**: User Interface - Build the frontend
- **Phase 7**: Testing & Optimization - End-to-end testing and performance tuning

## License

Part of the AI Restaurant Recommendation Service project.

## Support

For issues or questions:
1. Check this README
2. Review test files for usage examples
3. Check Groq API documentation: https://console.groq.com/docs
4. Review error logs for specific issues

## API Reference

### LLMService

```python
class LLMService:
    def __init__(self, config: Optional[LLMConfig] = None)
    def generate_recommendations(
        self,
        preferences: Dict[str, Any],
        restaurants: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[Dict[str, Any]]
    def generate_fallback_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[Dict[str, Any]]
    def health_check(self) -> Dict[str, Any]
```

### PromptBuilder

```python
class PromptBuilder:
    def build_recommendation_prompt(
        self,
        preferences: Dict[str, Any],
        restaurants: List[Dict[str, Any]],
        limit: int = 5
    ) -> str
    def build_fallback_prompt(
        self,
        preferences: Dict[str, Any],
        error_message: str
    ) -> str
```

### LLMConfig

```python
@dataclass
class LLMConfig:
    api_key: str
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 1024
    max_retries: int = 3
    retry_delay: float = 1.0
    
    @classmethod
    def from_env(cls) -> "LLMConfig"
    def validate(self) -> None
```

# End-to-End Testing Suite

## Overview

This directory contains comprehensive end-to-end tests for the AI Restaurant Recommendation Service. These tests validate the complete system from user input through all phases to final recommendations.

## Test Coverage

### 1. Critical User Journeys
- Complete recommendation flow (preferences → recommendations)
- Database query workflows
- LLM integration workflows
- Health check and monitoring flows

### 2. Happy Path Scenarios
- Valid preferences with all filters
- Valid preferences with minimal filters
- Default value application
- Successful LLM recommendations

### 3. Edge Cases
- Empty/missing preferences
- Boundary values (min/max ratings, prices)
- No matching restaurants
- LLM service failures and fallbacks
- Database connection issues

### 4. Error States
- Invalid input validation
- API error responses
- Service unavailability
- Timeout scenarios

### 5. API Validations
- Request/response format validation
- HTTP status codes
- Error message formats
- CORS headers

## Test Structure

```
End to End Testing/
├── README.md                           # This file
├── conftest.py                         # Shared fixtures and configuration
├── test_e2e_complete_flow.py          # Complete user journey tests
├── test_e2e_api_endpoints.py          # API endpoint integration tests
├── test_e2e_preference_validation.py  # Preference processing tests
├── test_e2e_database_integration.py   # Database integration tests
├── test_e2e_llm_integration.py        # LLM service integration tests
├── test_e2e_error_handling.py         # Error scenarios and edge cases
├── test_e2e_performance.py            # Performance and load tests
└── test_e2e_security.py               # Security and validation tests
```

## Running Tests

### Run All E2E Tests
```bash
cd "End to End Testing"
pytest -v
```

### Run Specific Test File
```bash
pytest test_e2e_complete_flow.py -v
```

### Run with Coverage
```bash
pytest --cov=../restaurant-recommendation --cov-report=html
```

### Run with Detailed Output
```bash
pytest -vv -s
```

## Prerequisites

1. **Phase 1 Database**: Must be populated with test data
   ```bash
   cd restaurant-recommendation/phase-1-data-pipeline
   python src/main.py
   ```

2. **API Server**: Must be running on localhost:8000
   ```bash
   cd restaurant-recommendation/phase-2-recommendation-api
   python src/main.py
   ```

3. **Environment Variables**: Groq API key configured (optional for LLM tests)
   ```bash
   # In phase-4-llm-integration/.env
   GROQ_API_KEY=your_api_key_here
   ```

## Test Categories

### Complete Flow Tests (`test_e2e_complete_flow.py`)
- End-to-end user journey from input to recommendations
- Multi-step workflows
- Data flow validation across all phases

### API Endpoint Tests (`test_e2e_api_endpoints.py`)
- All REST API endpoints
- Request/response validation
- HTTP status codes
- CORS and headers

### Preference Validation Tests (`test_e2e_preference_validation.py`)
- Input validation rules
- Normalization logic
- Default value application
- Error message accuracy

### Database Integration Tests (`test_e2e_database_integration.py`)
- Database connectivity
- Query accuracy
- Filter combinations
- Data integrity

### LLM Integration Tests (`test_e2e_llm_integration.py`)
- LLM service connectivity
- Prompt generation
- Response parsing
- Fallback mechanisms

### Error Handling Tests (`test_e2e_error_handling.py`)
- Invalid inputs
- Service failures
- Timeout scenarios
- Graceful degradation

### Performance Tests (`test_e2e_performance.py`)
- Response time benchmarks
- Concurrent request handling
- Database query performance
- LLM latency

### Security Tests (`test_e2e_security.py`)
- Input sanitization
- SQL injection prevention
- XSS prevention
- Rate limiting

## Test Data

Tests use the production database from Phase 1. Ensure it contains:
- Multiple cuisines (Italian, Chinese, Mexican, etc.)
- Multiple locations (Downtown, Uptown, Midtown)
- Varied ratings (0.0 - 5.0)
- Varied prices

## Expected Results

All tests should pass when:
- ✅ Phase 1 database is populated
- ✅ API server is running
- ✅ All dependencies are installed
- ✅ Environment variables are configured

## Troubleshooting

### Tests Fail: "Connection refused"
**Solution**: Start the API server first
```bash
cd restaurant-recommendation/phase-2-recommendation-api
python src/main.py
```

### Tests Fail: "Database not found"
**Solution**: Run Phase 1 pipeline to create database
```bash
cd restaurant-recommendation/phase-1-data-pipeline
python src/main.py
```

### LLM Tests Fail
**Solution**: Check Groq API key is configured
```bash
# Verify .env file exists
cat restaurant-recommendation/phase-4-llm-integration/.env
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run E2E Tests
  run: |
    cd "End to End Testing"
    pytest -v --junitxml=test-results.xml
```

## Contributing

When adding new tests:
1. Follow existing naming conventions
2. Add clear docstrings explaining what is tested
3. Include both positive and negative test cases
4. Update this README with new test categories

## License

Part of the AI Restaurant Recommendation Service project.

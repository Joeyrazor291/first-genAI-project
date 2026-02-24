# Quick Start Guide - End-to-End Testing

## Prerequisites

1. **Python 3.8+** installed
2. **Phase 1 Database** populated with data
3. **API Server** running on localhost:8000

## Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd "End to End Testing"
pip install -r requirements.txt
```

### Step 2: Start the API Server

Open a new terminal window:

```bash
cd restaurant-recommendation/phase-2-recommendation-api
python src/main.py
```

Wait for the message: `Uvicorn running on http://0.0.0.0:8000`

### Step 3: Verify Database

Ensure Phase 1 database exists:

```bash
# Check if database file exists
dir ..\restaurant-recommendation\phase-1-data-pipeline\data\restaurant.db
```

If not found, create it:

```bash
cd ..\restaurant-recommendation\phase-1-data-pipeline
python src\main.py
```

## Running Tests

### Run All Tests

```bash
pytest -v
```

### Run Specific Test Categories

```bash
# Complete flow tests
pytest test_e2e_complete_flow.py -v

# API endpoint tests
pytest test_e2e_api_endpoints.py -v

# Preference validation tests
pytest test_e2e_preference_validation.py -v

# Database integration tests
pytest test_e2e_database_integration.py -v

# Error handling tests
pytest test_e2e_error_handling.py -v

# LLM integration tests (requires API key)
pytest test_e2e_llm_integration.py -v

# Performance tests (slow)
pytest test_e2e_performance.py -v

# Security tests
pytest test_e2e_security.py -v
```

### Run Tests by Marker

```bash
# Run only fast tests (exclude slow tests)
pytest -m "not slow" -v

# Run only tests that require API
pytest -m "requires_api" -v

# Run only LLM tests
pytest -m "requires_llm" -v
```

### Run with Coverage

```bash
pytest --cov=../restaurant-recommendation --cov-report=html
```

View coverage report: Open `htmlcov/index.html` in browser

### Run Tests in Parallel

```bash
# Run tests using 4 workers
pytest -n 4
```

## Expected Results

### Successful Test Run

```
======================== test session starts ========================
collected 150+ items

test_e2e_complete_flow.py::TestCompleteUserJourney::test_complete_flow_with_all_filters PASSED
test_e2e_complete_flow.py::TestCompleteUserJourney::test_complete_flow_minimal_input PASSED
...
======================== 150+ passed in 45.23s ========================
```

### Test Summary

- **Total Tests**: 150+
- **Expected Duration**: 30-60 seconds (without slow tests)
- **Expected Pass Rate**: 100% (when API is running)

## Common Issues

### Issue: "Connection refused"

**Problem**: API server not running

**Solution**:
```bash
cd restaurant-recommendation/phase-2-recommendation-api
python src/main.py
```

### Issue: "Database not found"

**Problem**: Phase 1 database doesn't exist

**Solution**:
```bash
cd restaurant-recommendation/phase-1-data-pipeline
python src/main.py
```

### Issue: "Module not found"

**Problem**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: LLM tests fail

**Problem**: Groq API key not configured

**Solution**: LLM tests are optional. Skip them:
```bash
pytest -m "not requires_llm" -v
```

Or configure API key:
```bash
# In restaurant-recommendation/phase-4-llm-integration/.env
GROQ_API_KEY=your_api_key_here
```

## Test Output Examples

### Successful Test

```
test_e2e_complete_flow.py::TestCompleteUserJourney::test_complete_flow_with_all_filters 
✓ API server is ready
✓ Complete pipeline executed in 2.34s
PASSED
```

### Failed Test

```
test_e2e_api_endpoints.py::TestHealthEndpoint::test_health_check_returns_healthy_status 
FAILED - AssertionError: Expected status 'healthy', got 'unhealthy'
```

## Advanced Usage

### Generate HTML Report

```bash
pytest --html=report.html --self-contained-html
```

### Generate JSON Report

```bash
pytest --json-report --json-report-file=report.json
```

### Run Specific Test

```bash
pytest test_e2e_complete_flow.py::TestCompleteUserJourney::test_complete_flow_with_all_filters -v
```

### Run Tests with Timeout

```bash
pytest --timeout=300  # 5 minute timeout per test
```

### Verbose Output with Print Statements

```bash
pytest -v -s
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        cd "End to End Testing"
        pip install -r requirements.txt
    
    - name: Setup database
      run: |
        cd restaurant-recommendation/phase-1-data-pipeline
        pip install -r requirements.txt
        python src/main.py
    
    - name: Start API server
      run: |
        cd restaurant-recommendation/phase-2-recommendation-api
        pip install -r requirements.txt
        python src/main.py &
        sleep 5
    
    - name: Run tests
      run: |
        cd "End to End Testing"
        pytest -v --junitxml=test-results.xml
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: test-results.xml
```

## Performance Benchmarks

Expected performance on typical hardware:

| Test Category | Tests | Duration | Pass Rate |
|--------------|-------|----------|-----------|
| Complete Flow | 15 | 10-15s | 100% |
| API Endpoints | 30 | 5-10s | 100% |
| Preference Validation | 25 | 3-5s | 100% |
| Database Integration | 20 | 5-8s | 100% |
| Error Handling | 30 | 8-12s | 100% |
| LLM Integration | 20 | 15-30s | 95%+ |
| Performance | 15 | 30-60s | 95%+ |
| Security | 25 | 10-15s | 100% |

## Next Steps

1. **Review test results** - Check which tests passed/failed
2. **Fix any failures** - Address issues in the application code
3. **Add custom tests** - Extend test suite for your specific needs
4. **Integrate with CI/CD** - Automate testing in your pipeline
5. **Monitor coverage** - Aim for 80%+ code coverage

## Support

For issues or questions:
1. Check the main README.md
2. Review test file docstrings
3. Check API documentation at http://localhost:8000/api/v1/docs

## License

Part of the AI Restaurant Recommendation Service project.

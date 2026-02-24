# Phase 2: Recommendation API - AI Restaurant Recommendation Service

## Purpose and Scope

Phase 2 builds the RESTful API layer on top of Phase 1's data pipeline. This phase provides:

- REST API endpoints for restaurant recommendations
- User preference validation and normalization
- Integration with Phase 1 database
- OpenAPI documentation
- Comprehensive error handling

This phase does NOT include LLM integration or frontend components. Those will be implemented in subsequent phases.

## Prerequisites

**Phase 1 must be completed first!** Phase 2 depends on the Phase 1 database.

```bash
# Run Phase 1 pipeline first
cd ../phase-1-data-pipeline
pip install -r requirements.txt
py -m src.main  # or py verify_implementation.py for demo data
```

## Folder Structure

```
phase-2-recommendation-api/
├── src/
│   ├── __init__.py
│   ├── main.py                  # Server entry point
│   ├── api.py                   # FastAPI application
│   ├── config.py                # Configuration
│   ├── models.py                # Pydantic models
│   ├── preference_processor.py  # Preference validation
│   └── database.py              # Phase 1 database integration
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── test_api.py              # API endpoint tests
│   ├── test_preference_processor.py  # Validation tests
│   └── test_database.py         # Database service tests
├── .env                         # Local config (not committed)
├── .env.example                 # Config template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Setup Instructions

### 1. Navigate to Phase 2 Directory

```bash
cd restaurant-recommendation/phase-2-recommendation-api
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env  # Windows
# or
cp .env.example .env    # macOS/Linux

# Edit .env if needed (default values should work)
```

## Running the API Server

### Start the Server

```bash
py -m src.main
```

The server will start on `http://localhost:8000`

### Access API Documentation

Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc
- **OpenAPI JSON:** http://localhost:8000/api/v1/openapi.json

## API Endpoints

### 1. Root Endpoint

```
GET /
```

Returns API information and available endpoints.

**Example:**
```bash
curl http://localhost:8000/
```

### 2. Health Check

```
GET /health
```

Check API and database health status.

**Example:**
```bash
curl http://localhost:8000/health
```

### 3. Get Recommendations

```
POST /api/v1/recommendations
```

Get restaurant recommendations based on preferences.

**Request Body:**
```json
{
  "cuisine": "italian",
  "location": "downtown",
  "min_rating": 4.0,
  "max_price": 30.0,
  "limit": 5
}
```

**All fields are optional:**
- `cuisine` (string): Filter by cuisine type
- `location` (string): Filter by location
- `min_rating` (float): Minimum rating (0.0-5.0)
- `max_price` (float): Maximum price
- `limit` (int): Max results (1-100, default: 10)

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{"cuisine": "italian", "min_rating": 4.0, "limit": 5}'
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "recommendations": [
    {
      "id": 1,
      "name": "Bella Italia",
      "cuisine": "italian",
      "location": "downtown",
      "rating": 4.5,
      "price": 25.50
    }
  ],
  "filters_applied": {
    "cuisine": "italian",
    "min_rating": 4.0,
    "limit": 5
  }
}
```

### 4. List All Restaurants

```
GET /api/v1/restaurants?limit=50
```

Get a list of all restaurants.

**Query Parameters:**
- `limit` (int): Max results (default: 50, max: 100)

**Example:**
```bash
curl http://localhost:8000/api/v1/restaurants?limit=10
```

### 5. Get Statistics

```
GET /api/v1/stats
```

Get database statistics.

**Example:**
```bash
curl http://localhost:8000/api/v1/stats
```

**Response:**
```json
{
  "total_restaurants": 1000,
  "unique_cuisines": 25,
  "unique_locations": 15
}
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v --tb=short
```

### Run Specific Test Files

```bash
# Test API endpoints
pytest tests/test_api.py -v

# Test preference processor
pytest tests/test_preference_processor.py -v

# Test database service
pytest tests/test_database.py -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

The test suite includes:

### API Tests (`test_api.py`)
- Root endpoint returns API info
- Health check endpoint
- Recommendations with all filters
- Recommendations with minimal filters
- Filter by cuisine, location, rating, price
- Combined filters
- No matches scenario
- Invalid input validation
- Limit parameter enforcement
- Response model validation

### Preference Processor Tests (`test_preference_processor.py`)
- Validate all preferences
- Validate minimal preferences
- Invalid rating validation
- Invalid price validation
- Invalid limit validation
- Text field normalization
- Default value application
- Filter summary generation

### Database Service Tests (`test_database.py`)
- Service initialization
- Store property lazy loading
- Missing database error handling
- Get recommendations with filters
- Get statistics
- Get all restaurants
- Connection closing

## Configuration

The `.env` file supports:

```env
# API Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Phase 1 Database Path (relative to phase-2-recommendation-api/)
PHASE1_DB_PATH=../phase-1-data-pipeline/data/restaurant.db

# Logging Level
LOG_LEVEL=INFO
```

## Usage Examples

### Python Requests

```python
import requests

# Get recommendations
response = requests.post(
    'http://localhost:8000/api/v1/recommendations',
    json={
        'cuisine': 'italian',
        'min_rating': 4.0,
        'max_price': 30.0,
        'limit': 5
    }
)

data = response.json()
for restaurant in data['recommendations']:
    print(f"{restaurant['name']}: {restaurant['rating']} stars, ${restaurant['price']}")
```

### JavaScript Fetch

```javascript
fetch('http://localhost:8000/api/v1/recommendations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    cuisine: 'italian',
    min_rating: 4.0,
    limit: 5
  })
})
.then(response => response.json())
.then(data => {
  console.log(`Found ${data.count} restaurants`);
  data.recommendations.forEach(r => {
    console.log(`${r.name}: ${r.rating} stars`);
  });
});
```

### cURL

```bash
# Get Italian restaurants rated 4.0+
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{"cuisine": "italian", "min_rating": 4.0}'

# Get statistics
curl http://localhost:8000/api/v1/stats

# Health check
curl http://localhost:8000/health
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid input (validation error)
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Database unavailable

**Error Response Format:**
```json
{
  "detail": "min_rating must be between 0.0 and 5.0"
}
```

## Architecture

### Components

1. **API Layer** (`api.py`)
   - FastAPI application
   - Endpoint definitions
   - Request/response handling
   - Error handling middleware

2. **Models** (`models.py`)
   - Pydantic models for validation
   - Request/response schemas
   - Data validation rules

3. **Preference Processor** (`preference_processor.py`)
   - Input validation
   - Default value application
   - Filter normalization

4. **Database Service** (`database.py`)
   - Integration with Phase 1
   - Query orchestration
   - Connection management

### Data Flow

```
Client Request
    ↓
FastAPI Endpoint
    ↓
Pydantic Validation (models.py)
    ↓
Preference Processor (preference_processor.py)
    ↓
Database Service (database.py)
    ↓
Phase 1 RestaurantStore
    ↓
SQLite Database
    ↓
Response to Client
```

## What Phase 3 Will Build

Phase 3 will implement **LLM Integration** for intelligent recommendations:

- LLM prompt engineering
- Context-aware recommendation generation
- Fallback mechanisms
- Response parsing
- Integration with Phase 2 API

Phase 3 will enhance the `/api/v1/recommendations` endpoint with LLM-powered insights.

## Troubleshooting

### Issue: Database not found
**Error:** `Phase 1 database not found`  
**Solution:** Run Phase 1 pipeline first:
```bash
cd ../phase-1-data-pipeline
py -m src.main
```

### Issue: Import errors
**Error:** `ModuleNotFoundError: No module named 'src'`  
**Solution:** Run as module: `py -m src.main` (not `py src/main.py`)

### Issue: Port already in use
**Error:** `Address already in use`  
**Solution:** Change port in `.env` file or stop the process using port 8000

### Issue: Tests fail
**Problem:** Some tests fail  
**Solution:** Ensure Phase 1 is set up and virtual environment is activated

## Performance

- **API Response Time:** < 100ms for typical queries
- **Concurrent Requests:** Supports multiple simultaneous requests
- **Database Queries:** Optimized with indexes from Phase 1

## Security Considerations

Current implementation (Phase 2):
- Input validation via Pydantic
- SQL injection protection via SQLAlchemy
- CORS enabled for development

Future phases will add:
- Authentication & authorization
- Rate limiting
- API keys
- Request throttling

## Exit Criteria

Phase 2 is complete when:

- ✅ All API endpoints functional
- ✅ All tests pass (40+ test cases)
- ✅ OpenAPI documentation generated
- ✅ Integration with Phase 1 database working
- ✅ Error handling comprehensive
- ✅ README complete

## License

This is part of the AI Restaurant Recommendation Service project.

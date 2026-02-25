# Starting the Project with Groq LLM API

This guide walks you through starting the AI Restaurant Recommendation Service with **Groq** as the LLM provider.

---

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- Groq API key (free tier available at https://console.groq.com)

---

## Step 1: Get Your Groq API Key

1. Visit https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

---

## Step 2: Configure Groq API

### Update the LLM Configuration

Edit `restaurant-recommendation/phase-4-llm-integration/.env`:

```env
# LLM Provider Configuration
LLM_PROVIDER=groq

# Groq Configuration
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# LLM Model Configuration
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY=1.0
```

Replace `gsk_your_api_key_here` with your actual Groq API key.

---

## Step 3: Install Dependencies

### Install All Project Dependencies

```bash
# Install E2E testing dependencies
pip install -r "End to End Testing/requirements.txt"

# Install Phase 1 (Data Pipeline)
pip install -r "restaurant-recommendation/phase-1-data-pipeline/requirements.txt"

# Install Phase 2 (API)
pip install -r "restaurant-recommendation/phase-2-recommendation-api/requirements.txt"

# Install Phase 4 (LLM Integration)
pip install -r "restaurant-recommendation/phase-4-llm-integration/requirements.txt"

# Install Frontend dependencies (if running frontend)
cd restaurant-recommendation/phase-6-frontend
npm install
cd ../..
```

---

## Step 4: Start the API Server

Open a terminal and run:

```bash
cd restaurant-recommendation/phase-2-recommendation-api
py -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## Step 5: Start the Frontend (Optional)

Open another terminal and run:

```bash
cd restaurant-recommendation/phase-6-frontend
npm run dev
```

The frontend will be available at: **http://localhost:5173**

---

## Step 6: Access the Application

### Option A: Use the Frontend UI
- Open http://localhost:5173 in your browser
- Enter your dining preferences
- Click "Get Recommendations"
- View AI-powered recommendations with Groq explanations

### Option B: Use the API Directly

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Get Recommendations
```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "cuisine": "italian",
    "min_rating": 4.0,
    "limit": 5
  }'
```

#### API Documentation
Open http://localhost:8000/api/v1/docs in your browser

---

## Step 7: Run End-to-End Tests

### Run All Tests
```bash
cd "End to End Testing"
pytest -v
```

### Run Fast Tests Only
```bash
pytest -m "not slow" -v
```

### Run Specific Test Categories
```bash
# API tests
pytest test_e2e_api_endpoints.py -v

# LLM tests (with Groq)
pytest test_e2e_llm_integration.py -v

# Complete flow tests
pytest test_e2e_complete_flow.py -v
```

### Run with Coverage
```bash
pytest --cov=../restaurant-recommendation --cov-report=html
```

---

## Groq API Configuration Details

### Model Options

Groq supports several models. The default is optimized for speed:

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| llama-3.3-70b-versatile | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Excellent | Recommended |
| llama-3.1-70b-versatile | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Excellent | Alternative |
| mixtral-8x7b-32768 | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Budget option |

### Configuration Parameters

```env
# Temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
LLM_TEMPERATURE=0.7

# Max Tokens: Maximum response length
LLM_MAX_TOKENS=1024

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY=1.0
```

### Groq Advantages

✅ **Free Tier**: Generous free tier with no credit card required
✅ **Speed**: Extremely fast inference (often < 1 second)
✅ **Quality**: Excellent model quality with Llama 3.3 70B
✅ **Reliability**: Stable API with good uptime
✅ **Cost**: Very affordable pricing

---

## Example Usage

### Frontend Example

1. Open http://localhost:5173
2. Enter preferences:
   - Cuisine: "Italian"
   - Min Rating: 4.0
   - Max Price: 30
   - Limit: 5
3. Click "Get Recommendations"
4. View results with Groq-generated explanations

### API Example

```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "cuisine": "italian",
    "location": "downtown",
    "min_rating": 4.0,
    "max_price": 30.0,
    "limit": 5
  }'
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "recommendations": [
    {
      "name": "The Pizza Bakery",
      "cuisine": "Italian",
      "location": "Downtown",
      "rating": 4.8,
      "price": 600,
      "explanation": "The Pizza Bakery is recommended because it serves Italian cuisine with a high rating of 4.8/5.0, exceeding the user's minimum rating requirement of 4.0/5.0. The restaurant is located in Downtown, matching the user's location preference..."
    },
    ...
  ],
  "filters_applied": {
    "cuisine": "italian",
    "location": "downtown",
    "min_rating": 4.0,
    "max_price": 30.0,
    "limit": 5
  }
}
```

---

## Troubleshooting

### Issue: "Invalid API Key"

**Solution**: 
- Verify your Groq API key is correct
- Check that it starts with `gsk_`
- Ensure there are no extra spaces in the `.env` file

### Issue: "Rate limit exceeded"

**Solution**:
- Groq has rate limits on free tier
- Wait a few seconds before making another request
- Consider upgrading to paid tier for higher limits

### Issue: "Model not found"

**Solution**:
- Verify the model name is correct: `llama-3.3-70b-versatile`
- Check Groq console for available models
- Update the model name in `.env`

### Issue: "Connection timeout"

**Solution**:
- Check your internet connection
- Verify Groq API is accessible: https://console.groq.com
- Try again in a few moments

### Issue: "API server won't start"

**Solution**:
- Ensure port 8000 is not in use
- Check all dependencies are installed
- Verify `.env` file exists and is readable

### Issue: "Tests timeout"

**Solution**:
- Ensure API server is running on port 8000
- Check Groq API is accessible
- Increase timeout: `pytest --timeout=60`

---

## Performance Metrics

With Groq LLM:

| Operation | Time |
|-----------|------|
| API Response (no LLM) | < 100ms |
| LLM Explanation (Groq) | 1-3 seconds |
| Database Query | < 50ms |
| Frontend Load | < 2 seconds |
| Health Check | < 50ms |

Groq is typically **faster** than OpenRouter due to its optimized inference engine.

---

## Project Architecture

```
User Input (Frontend)
    ↓
API Request (Phase 2)
    ↓
Validate Input (Phase 3)
    ↓
Filter Restaurants (Phase 1 + Phase 5)
    ↓
Generate Explanations (Phase 4 - Groq LLM)
    ↓
Return Results (Phase 2)
    ↓
Display UI (Phase 6)
```

---

## Database Information

- **Total Restaurants**: 9,216
- **Unique Cuisines**: 85
- **Unique Locations**: 92
- **Average Rating**: 3.63/5.0
- **Average Price**: $268.50

---

## API Endpoints

### Health Check
```
GET /health
```

### Get Recommendations
```
POST /api/v1/recommendations
Content-Type: application/json

{
  "cuisine": "italian",
  "location": "downtown",
  "min_rating": 4.0,
  "max_price": 30.0,
  "limit": 5
}
```

### List Restaurants
```
GET /api/v1/restaurants?limit=50
```

### Database Statistics
```
GET /api/v1/stats
```

### API Documentation
```
http://localhost:8000/api/v1/docs
```

---

## Switching to OpenRouter

If you want to switch to OpenRouter instead:

1. Edit `restaurant-recommendation/phase-4-llm-integration/.env`
2. Change `LLM_PROVIDER=groq` to `LLM_PROVIDER=openrouter`
3. Ensure `OPENROUTER_API_KEY` is set
4. Restart the API server

See `START_WITH_OPENROUTER.md` for detailed OpenRouter setup.

---

## Next Steps

1. ✅ Configure Groq API key
2. ✅ Install dependencies
3. ✅ Start API server
4. ✅ Start frontend (optional)
5. ✅ Access application
6. ✅ Run tests

---

## Support & Documentation

- **Groq Console**: https://console.groq.com
- **Groq API Docs**: https://console.groq.com/docs
- **Project README**: `README.md`
- **API Documentation**: http://localhost:8000/api/v1/docs (when running)
- **Test Guide**: `E2E_TEST_EXECUTION_GUIDE.md`

---

## Status

✅ **Project configured with Groq LLM**

- LLM Provider: ✅ Groq
- Model: ✅ llama-3.3-70b-versatile
- Database: ✅ 9,216 restaurants
- API: ✅ Ready to start
- Frontend: ✅ Ready to start
- Tests: ✅ 150+ tests available


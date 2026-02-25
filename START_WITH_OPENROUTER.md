# Starting the Project with OpenRouter LLM API

This guide walks you through starting the AI Restaurant Recommendation Service with **OpenRouter** as the LLM provider.

---

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- OpenRouter API key (https://openrouter.ai)

---

## Step 1: Get Your OpenRouter API Key

1. Visit https://openrouter.ai
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-`)

---

## Step 2: Configure OpenRouter API

### Update the LLM Configuration

Edit `restaurant-recommendation/phase-4-llm-integration/.env`:

```env
# LLM Provider Configuration
LLM_PROVIDER=openrouter

# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your_api_key_here
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct

# LLM Model Configuration
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY=1.0
```

Replace `sk-or-v1-your_api_key_here` with your actual OpenRouter API key.

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
- View AI-powered recommendations with OpenRouter explanations

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

# LLM tests (with OpenRouter)
pytest test_e2e_llm_integration.py -v

# Complete flow tests
pytest test_e2e_complete_flow.py -v
```

### Run with Coverage
```bash
pytest --cov=../restaurant-recommendation --cov-report=html
```

---

## OpenRouter API Configuration Details

### Model Options

OpenRouter provides access to multiple models. The default is optimized for quality:

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| meta-llama/llama-3.3-70b-instruct | ⚡⚡ Fast | ⭐⭐⭐⭐ Excellent | $ | Recommended |
| meta-llama/llama-3.1-70b-instruct | ⚡⚡ Fast | ⭐⭐⭐⭐ Excellent | $ | Alternative |
| openai/gpt-4-turbo | ⚡ Slower | ⭐⭐⭐⭐⭐ Best | $$$ | Premium |
| anthropic/claude-3-opus | ⚡ Slower | ⭐⭐⭐⭐⭐ Best | $$$ | Premium |

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

### OpenRouter Advantages

✅ **Model Variety**: Access to 100+ models from different providers
✅ **Flexibility**: Switch between models easily
✅ **Quality**: Premium models like GPT-4 and Claude available
✅ **Fallback**: Automatic fallback to alternative models
✅ **Transparency**: Clear pricing per model

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
4. View results with OpenRouter-generated explanations

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
- Verify your OpenRouter API key is correct
- Check that it starts with `sk-or-v1-`
- Ensure there are no extra spaces in the `.env` file
- Regenerate the key if needed at https://openrouter.ai

### Issue: "Model not found"

**Solution**:
- Verify the model name is correct: `meta-llama/llama-3.3-70b-instruct`
- Check available models at https://openrouter.ai/docs/models
- Update the model name in `.env`

### Issue: "Insufficient credits"

**Solution**:
- Check your OpenRouter account balance
- Add credits at https://openrouter.ai/account/billing/overview
- Consider using a cheaper model

### Issue: "Rate limit exceeded"

**Solution**:
- OpenRouter has rate limits based on your plan
- Wait a few seconds before making another request
- Upgrade your plan for higher limits

### Issue: "Connection timeout"

**Solution**:
- Check your internet connection
- Verify OpenRouter API is accessible: https://openrouter.ai
- Try again in a few moments

### Issue: "API server won't start"

**Solution**:
- Ensure port 8000 is not in use
- Check all dependencies are installed
- Verify `.env` file exists and is readable

### Issue: "Tests timeout"

**Solution**:
- Ensure API server is running on port 8000
- Check OpenRouter API is accessible
- Increase timeout: `pytest --timeout=60`

---

## Performance Metrics

With OpenRouter LLM:

| Operation | Time |
|-----------|------|
| API Response (no LLM) | < 100ms |
| LLM Explanation (OpenRouter) | 2-5 seconds |
| Database Query | < 50ms |
| Frontend Load | < 2 seconds |
| Health Check | < 50ms |

Performance varies by model. Llama 3.3 70B is typically faster than GPT-4.

---

## Switching Models

To use a different model with OpenRouter:

1. Edit `restaurant-recommendation/phase-4-llm-integration/.env`
2. Change `OPENROUTER_MODEL` to desired model
3. Restart the API server

Example models:
```env
# Fast & Good Quality
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct

# Premium Quality
OPENROUTER_MODEL=openai/gpt-4-turbo

# Budget Option
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

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
Generate Explanations (Phase 4 - OpenRouter LLM)
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

## Switching to Groq

If you want to switch to Groq instead:

1. Edit `restaurant-recommendation/phase-4-llm-integration/.env`
2. Change `LLM_PROVIDER=openrouter` to `LLM_PROVIDER=groq`
3. Ensure `GROQ_API_KEY` is set
4. Restart the API server

See `START_WITH_GROQ.md` for detailed Groq setup.

---

## Next Steps

1. ✅ Configure OpenRouter API key
2. ✅ Install dependencies
3. ✅ Start API server
4. ✅ Start frontend (optional)
5. ✅ Access application
6. ✅ Run tests

---

## Support & Documentation

- **OpenRouter Website**: https://openrouter.ai
- **OpenRouter API Docs**: https://openrouter.ai/docs
- **OpenRouter Models**: https://openrouter.ai/docs/models
- **Project README**: `README.md`
- **API Documentation**: http://localhost:8000/api/v1/docs (when running)
- **Test Guide**: `E2E_TEST_EXECUTION_GUIDE.md`

---

## Status

✅ **Project configured with OpenRouter LLM**

- LLM Provider: ✅ OpenRouter
- Model: ✅ meta-llama/llama-3.3-70b-instruct
- Database: ✅ 9,216 restaurants
- API: ✅ Ready to start
- Frontend: ✅ Ready to start
- Tests: ✅ 150+ tests available


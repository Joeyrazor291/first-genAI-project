# AI Restaurant Recommendation Service
- An recommendation service created by amit subudhi as a PM for learning and using it in his own accords
A full-stack AI-powered restaurant recommendation system with 6 integrated phases.

## 🚀 Quick Start

### Open Your Browser
```
http://localhost:5173
```

**That's it! The application is fully operational.**

---

## 📊 System Status

| Component | Port | Status |
|-----------|------|--------|
| Frontend UI | 5173 | ✅ Running |
| Backend API | 8000 | ✅ Running |
| Database | - | ✅ Connected |
| LLM Service | - | ✅ Active |

---

## 📚 Documentation

### Getting Started
- **[PROJECT_READY.md](PROJECT_READY.md)** - Start here! Quick overview and how to use
- **[START_PROJECT.md](START_PROJECT.md)** - Complete startup guide with all details
- **[RUNNING_SERVICES.md](RUNNING_SERVICES.md)** - Current services and architecture
- **[SYSTEM_VERIFICATION.md](SYSTEM_VERIFICATION.md)** - Detailed system verification report

---

## 🎯 What This Does

Enter your dining preferences and get AI-powered restaurant recommendations with:
- Restaurant name, cuisine, location
- Rating and price information
- **AI-generated explanation** of why it's recommended

### Example
```
Preference: Italian restaurants, min rating 4.0
Result: "The Pizza Bakery - Italian, 4.8★, $600
Explanation: The Pizza Bakery is recommended because it serves 
Italian cuisine with a high rating of 4.8/5.0, exceeding the 
user's minimum rating requirement of 4.0/5.0..."
```

---

## 🏗️ Architecture

### 6 Integrated Phases

1. **Phase 1: Data Pipeline**
   - 9,216 restaurants in SQLite database
   - 85 cuisine types, 92 locations

2. **Phase 2: Recommendation API**
   - FastAPI REST endpoints
   - Running on port 8000

3. **Phase 3: Preference Processing**
   - Input validation and normalization
   - Handles all filter types

4. **Phase 4: LLM Integration**
   - OpenRouter (Llama 3.3 70B)
   - Generates AI explanations

5. **Phase 5: Recommendation Engine**
   - Intelligent filtering
   - LLM-powered enrichment

6. **Phase 6: Frontend UI**
   - React + Vite
   - Running on port 5173

### Data Flow
```
User Input (Frontend)
    ↓
API Request (Phase 2)
    ↓
Validate Input (Phase 3)
    ↓
Filter Restaurants (Phase 1 + Phase 5)
    ↓
Generate Explanations (Phase 4)
    ↓
Return Results (Phase 2)
    ↓
Display UI (Phase 6)
```

---

## 🎨 How to Use

### 1. Open Frontend
```
http://localhost:5173
```

### 2. Enter Preferences (All Optional)
- Cuisine type (e.g., "italian")
- Location (e.g., "downtown")
- Min rating (0.0 - 5.0)
- Max price
- Number of results (1 - 100)

### 3. Get Recommendations
Click "Get Recommendations" button

### 4. View Results
See restaurants with AI-generated explanations

---

## 📡 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Get Recommendations
```bash
POST http://localhost:8000/api/v1/recommendations
Content-Type: application/json

{
  "cuisine": "italian",
  "min_rating": 4.0,
  "limit": 5
}
```

### List Restaurants
```bash
GET http://localhost:8000/api/v1/restaurants?limit=50
```

### Database Stats
```bash
GET http://localhost:8000/api/v1/stats
```

### API Documentation
```
http://localhost:8000/api/v1/docs
```

---

## 💾 Database

```
Total Restaurants: 9,216
Unique Cuisines: 85
Unique Locations: 92
Average Rating: 3.63/5.0
Average Price: $268.50
```

---

## ⚡ Performance

| Operation | Time |
|-----------|------|
| API Response (no LLM) | < 100ms |
| LLM Explanation | 2-5 seconds |
| Database Query | < 50ms |
| Frontend Load | < 2 seconds |

---

## 🔧 Configuration

### Phase 2 API
```env
API_HOST=0.0.0.0
API_PORT=8000
PHASE1_DB_PATH=../phase-1-data-pipeline/data/restaurant.db
LOG_LEVEL=INFO
```

### Phase 4 LLM
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
```

---

## 🐛 Troubleshooting

### API Shows as "Offline"
```bash
curl http://localhost:8000/health
```

### No Recommendations Found
1. Try with fewer filters
2. Check database: `curl http://localhost:8000/api/v1/stats`

### Slow Responses
- LLM takes 2-5 seconds (normal)
- Check internet connection

---

## 📁 Project Structure

```
restaurant-recommendation/
├── phase-1-data-pipeline/          # Database
├── phase-2-recommendation-api/     # FastAPI (Port 8000)
├── phase-3-preference-processing/  # Validation
├── phase-4-llm-integration/        # OpenRouter
├── phase-5-recommendation-engine/  # Filtering
└── phase-6-frontend/               # React UI (Port 5173)
```

---

## ✨ Features

- ✅ 9,216 restaurants in database
- ✅ 85 cuisine types
- ✅ 92 locations
- ✅ AI-powered explanations
- ✅ Real-time API status
- ✅ Responsive design
- ✅ Error handling
- ✅ Input validation

---

## 🎯 Next Steps

1. Open http://localhost:5173
2. Enter your dining preferences
3. Get AI-powered recommendations
4. Review restaurant details
5. Enjoy personalized suggestions

---

## 📖 More Information

- **[PROJECT_READY.md](PROJECT_READY.md)** - Quick overview
- **[START_PROJECT.md](START_PROJECT.md)** - Detailed setup
- **[RUNNING_SERVICES.md](RUNNING_SERVICES.md)** - Current services
- **[SYSTEM_VERIFICATION.md](SYSTEM_VERIFICATION.md)** - Verification report

---

## 🎉 Ready to Use!

**All systems are operational. Open http://localhost:5173 now!**

---

**Status: ✅ FULLY OPERATIONAL**

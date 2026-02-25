# Visual Guide - AI Restaurant Recommendation Service

Quick visual reference for the project structure and setup.

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│                      Port 5173                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  User Interface                                      │   │
│  │  - Preference Input Form                            │   │
│  │  - Recommendation Display                           │   │
│  │  - Real-time Results                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  API Server (FastAPI)                       │
│                      Port 8000                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Phase 2: Recommendation API                        │   │
│  │  - Health Check                                     │   │
│  │  - Get Recommendations                              │   │
│  │  - List Restaurants                                 │   │
│  │  - Database Stats                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┬───────────────────┐
        ↓                   ↓                   ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Phase 3    │  │   Phase 5    │  │   Phase 4    │
│ Preference   │  │ Recommendation│  │     LLM      │
│ Processing   │  │   Engine     │  │ Integration  │
│              │  │              │  │              │
│ - Validate   │  │ - Filter     │  │ - Groq       │
│ - Normalize  │  │ - Enrich     │  │ - OpenRouter │
│ - Transform  │  │ - Sort       │  │ - Generate   │
└──────────────┘  └──────────────┘  └──────────────┘
        ↓                   ↓                   ↓
        └───────────────────┬───────────────────┘
                            ↓
                ┌──────────────────────┐
                │   Phase 1: Database  │
                │   SQLite             │
                │                      │
                │ 9,216 Restaurants    │
                │ 85 Cuisines          │
                │ 92 Locations         │
                └──────────────────────┘
```

---

## 📁 Project Structure

```
restaurant-recommendation/
│
├── phase-1-data-pipeline/
│   ├── data/
│   │   └── restaurant.db          ← 9,216 restaurants
│   ├── src/
│   │   ├── data/
│   │   │   ├── ingestion.py
│   │   │   ├── preprocessing.py
│   │   │   └── store.py
│   │   └── main.py
│   └── tests/
│
├── phase-2-recommendation-api/
│   ├── src/
│   │   ├── api.py                 ← FastAPI app
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── phase-3-preference-processing/
│   ├── src/
│   │   └── preference_processor.py ← Input validation
│   └── tests/
│
├── phase-4-llm-integration/
│   ├── .env                        ← LLM Configuration
│   ├── src/
│   │   ├── llm_service.py         ← Groq/OpenRouter
│   │   ├── config.py
│   │   └── prompt_builder.py
│   └── tests/
│
├── phase-5-recommendation-engine/
│   ├── src/
│   │   └── engine.py              ← Filtering & enrichment
│   └── tests/
│
└── phase-6-frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── App.tsx
    ├── package.json
    └── vite.config.ts
```

---

## 🔄 Data Flow

```
User Input
    │
    ├─ Cuisine: "Italian"
    ├─ Location: "Downtown"
    ├─ Min Rating: 4.0
    ├─ Max Price: 30
    └─ Limit: 5
    │
    ↓
┌─────────────────────────────────┐
│  Phase 3: Validate & Normalize  │
│  - Check ranges                 │
│  - Normalize text               │
│  - Transform types              │
└─────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────┐
│  Phase 1: Query Database        │
│  - Filter by cuisine            │
│  - Filter by location           │
│  - Filter by rating             │
│  - Filter by price              │
│  - Sort by rating               │
│  - Limit results                │
└─────────────────────────────────┘
    │
    ↓ (9,216 restaurants → 5 matches)
    │
┌─────────────────────────────────┐
│  Phase 5: Enrich Results        │
│  - Add metadata                 │
│  - Format data                  │
│  - Prepare for LLM              │
└─────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────┐
│  Phase 4: Generate Explanations │
│  - Call LLM (Groq/OpenRouter)   │
│  - Generate explanations        │
│  - Parse responses              │
│  - Handle errors                │
└─────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────┐
│  Phase 2: Return Results        │
│  - Format response              │
│  - Add metadata                 │
│  - Return to frontend           │
└─────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────┐
│  Phase 6: Display Results       │
│  - Show recommendations         │
│  - Display explanations         │
│  - Show filters applied         │
│  - Allow new search             │
└─────────────────────────────────┘
```

---

## 🚀 Setup Flow

### Groq Setup (5 minutes)

```
1. Get API Key
   └─ https://console.groq.com
      └─ Copy: gsk_...

2. Update .env
   └─ LLM_PROVIDER=groq
   └─ GROQ_API_KEY=gsk_...

3. Install Dependencies
   └─ pip install -r requirements.txt

4. Start API Server
   └─ py -m uvicorn src.api:app --host 0.0.0.0 --port 8000

5. Access Application
   └─ http://localhost:8000/api/v1/docs
```

### OpenRouter Setup (10 minutes)

```
1. Get API Key
   └─ https://openrouter.ai
      └─ Copy: sk-or-v1-...

2. Add Credits
   └─ https://openrouter.ai/account/billing

3. Update .env
   └─ LLM_PROVIDER=openrouter
   └─ OPENROUTER_API_KEY=sk-or-v1-...

4. Install Dependencies
   └─ pip install -r requirements.txt

5. Start API Server
   └─ py -m uvicorn src.api:app --host 0.0.0.0 --port 8000

6. Access Application
   └─ http://localhost:8000/api/v1/docs
```

---

## 📊 Provider Comparison

```
┌──────────────────────────────────────────────────────────┐
│                    GROQ vs OPENROUTER                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  GROQ                          OPENROUTER               │
│  ────                          ──────────               │
│  ⚡⚡⚡ Fastest                ⚡⚡ Fast                 │
│  💰 Free                       💰 $0.001/req            │
│  ⭐ Easy Setup                 ⭐ Easy Setup            │
│  🎯 Limited Models             🎯 100+ Models           │
│  ⭐⭐⭐⭐ Quality              ⭐⭐⭐⭐⭐ Quality        │
│                                                          │
│  Best For:                     Best For:                │
│  ✓ Development                 ✓ Production             │
│  ✓ Testing                     ✓ Premium Models         │
│  ✓ Learning                    ✓ Flexibility            │
│  ✓ Free Tier                   ✓ Enterprise             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Quick Commands

```
┌─────────────────────────────────────────────────────────┐
│                   QUICK COMMANDS                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Start API Server:                                      │
│  $ cd restaurant-recommendation/phase-2-recommendation-api
│  $ py -m uvicorn src.api:app --host 0.0.0.0 --port 8000
│                                                         │
│  Start Frontend:                                        │
│  $ cd restaurant-recommendation/phase-6-frontend       │
│  $ npm run dev                                          │
│                                                         │
│  Run Tests:                                             │
│  $ cd "End to End Testing"                             │
│  $ pytest -v                                            │
│                                                         │
│  Check Health:                                          │
│  $ curl http://localhost:8000/health                   │
│                                                         │
│  Get Recommendations:                                   │
│  $ curl -X POST http://localhost:8000/api/v1/recommendations \
│    -H "Content-Type: application/json" \               │
│    -d '{"cuisine":"italian","limit":5}'                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation Map

```
┌─────────────────────────────────────────────────────────┐
│              DOCUMENTATION STRUCTURE                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  START HERE                                             │
│  ├─ QUICK_START_GUIDE.md (5 min)                       │
│  └─ RESTART_COMPLETE.md (Overview)                     │
│                                                         │
│  SETUP GUIDES                                           │
│  ├─ START_WITH_GROQ.md                                 │
│  └─ START_WITH_OPENROUTER.md                           │
│                                                         │
│  REFERENCE                                              │
│  ├─ LLM_PROVIDER_COMPARISON.md                         │
│  ├─ PROJECT_RESTART_SUMMARY.md                         │
│  ├─ README.md                                          │
│  └─ DOCUMENTATION_INDEX.md                             │
│                                                         │
│  TESTING                                                │
│  ├─ E2E_TEST_EXECUTION_GUIDE.md                        │
│  └─ E2E_TEST_SUMMARY.md                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints

```
┌─────────────────────────────────────────────────────────┐
│                   API ENDPOINTS                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Health Check                                           │
│  GET /health                                            │
│  └─ Returns: {"status": "healthy"}                     │
│                                                         │
│  Get Recommendations                                    │
│  POST /api/v1/recommendations                          │
│  └─ Body: {"cuisine": "italian", "limit": 5}          │
│  └─ Returns: List of recommendations with explanations │
│                                                         │
│  List Restaurants                                       │
│  GET /api/v1/restaurants?limit=50                      │
│  └─ Returns: List of restaurants                       │
│                                                         │
│  Database Statistics                                    │
│  GET /api/v1/stats                                     │
│  └─ Returns: {"total_restaurants": 9216, ...}         │
│                                                         │
│  Interactive Documentation                             │
│  GET /api/v1/docs                                      │
│  └─ Swagger UI for testing endpoints                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

```
┌─────────────────────────────────────────────────────────┐
│                  RESTAURANT TABLE                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  id (INTEGER PRIMARY KEY)                              │
│  name (TEXT)                                            │
│  cuisine (TEXT)                                         │
│  location (TEXT)                                        │
│  rating (REAL)                                          │
│  price (REAL)                                           │
│  description (TEXT)                                     │
│                                                         │
│  Statistics:                                            │
│  ├─ Total Restaurants: 9,216                           │
│  ├─ Unique Cuisines: 85                                │
│  ├─ Unique Locations: 92                               │
│  ├─ Average Rating: 3.63/5.0                           │
│  └─ Average Price: $268.50                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration

```
┌─────────────────────────────────────────────────────────┐
│              CONFIGURATION (.env)                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  LLM Provider Selection:                                │
│  LLM_PROVIDER=groq              (or openrouter)        │
│                                                         │
│  Groq Configuration:                                    │
│  GROQ_API_KEY=gsk_...                                  │
│  GROQ_MODEL=llama-3.3-70b-versatile                    │
│                                                         │
│  OpenRouter Configuration:                              │
│  OPENROUTER_API_KEY=sk-or-v1-...                       │
│  OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct    │
│                                                         │
│  LLM Parameters:                                        │
│  LLM_TEMPERATURE=0.7                                    │
│  LLM_MAX_TOKENS=1024                                    │
│  MAX_RETRIES=3                                          │
│  RETRY_DELAY=1.0                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing Overview

```
┌─────────────────────────────────────────────────────────┐
│                  TEST CATEGORIES                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ✓ API Endpoints (25 tests)                            │
│  ✓ Complete Flow (15 tests)                            │
│  ✓ Database Integration (30 tests)                     │
│  ✓ Error Handling (35 tests)                           │
│  ✓ LLM Integration (20 tests)                          │
│  ✓ Preference Validation (20 tests)                    │
│  ✓ React Frontend (20 tests)                           │
│  ✓ Security (30 tests)                                 │
│  ✓ Performance (15 tests - slow)                       │
│                                                         │
│  Total: 150+ tests                                      │
│  Duration: 30-60 seconds (without slow tests)          │
│  Pass Rate: 100% (when API is running)                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Decision Tree

```
                    START HERE
                        │
                        ↓
            Do you want to...?
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
    Get Started    Compare         Understand
    Quickly        Providers       Architecture
        │               │               │
        ↓               ↓               ↓
    QUICK_START    LLM_PROVIDER    README.md
    _GUIDE.md      _COMPARISON.md
        │               │               │
        ↓               ↓               ↓
    Choose          Choose          Choose
    Provider        Provider        Provider
        │               │               │
    ┌───┴───┐       ┌───┴───┐       ┌───┴───┐
    ↓       ↓       ↓       ↓       ↓       ↓
  Groq  OpenRouter Groq  OpenRouter Groq  OpenRouter
    │       │       │       │       │       │
    ↓       ↓       ↓       ↓       ↓       ↓
  START  START    START  START    START  START
  _WITH  _WITH    _WITH  _WITH    _WITH  _WITH
  _GROQ  _OPENR   _GROQ  _OPENR   _GROQ  _OPENR
  .md    OUTER    .md    OUTER    .md    OUTER
         .md             .md             .md
```

---

## 📈 Performance Timeline

```
User Request
    │
    ├─ API Processing: < 100ms
    │
    ├─ Database Query: < 50ms
    │
    ├─ LLM Processing:
    │  ├─ Groq: 1-3 seconds
    │  └─ OpenRouter: 2-5 seconds
    │
    ├─ Response Formatting: < 50ms
    │
    └─ Total Response Time:
       ├─ Groq: 1-3 seconds
       └─ OpenRouter: 2-5 seconds
```

---

## ✅ Verification Checklist

```
Before Starting:
☐ Python 3.8+ installed
☐ Node.js 16+ installed (for frontend)
☐ API key obtained (Groq or OpenRouter)
☐ .env file configured
☐ Dependencies installed

After Starting:
☐ API server running on port 8000
☐ Health check returns 200
☐ API docs accessible
☐ Tests passing
☐ Frontend running (optional)
```

---

## 🎉 You're Ready!

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ✅ Project Restarted                                  │
│  ✅ Dual LLM Support                                   │
│  ✅ Documentation Complete                             │
│  ✅ Tests Ready                                        │
│  ✅ API Ready                                          │
│                                                         │
│  Choose your provider and get started!                 │
│                                                         │
│  → START_WITH_GROQ.md                                  │
│  → START_WITH_OPENROUTER.md                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```


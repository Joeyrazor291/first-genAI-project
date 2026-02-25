# Restaurant Recommendation Engine - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APPLICATION                    │
│                      (Port 8501)                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              User Interface (Streamlit)                  │  │
│  │                                                          │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Sidebar                                        │   │  │
│  │  │  - Database Statistics                          │   │  │
│  │  │  - Health Status                               │   │  │
│  │  │  - Configuration Info                          │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Main Content                                  │   │  │
│  │  │  - Preference Form                             │   │  │
│  │  │    * Cuisine (multi-select)                    │   │  │
│  │  │    * Location (multi-select)                   │   │  │
│  │  │    * Min Rating (slider)                       │   │  │
│  │  │    * Max Price (slider)                        │   │  │
│  │  │    * Limit (number input)                      │   │  │
│  │  │  - Results Display                             │   │  │
│  │  │    * Restaurant Cards                          │   │  │
│  │  │    * AI Explanations                           │   │  │
│  │  │    * Filter Summary                            │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│                           ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Backend Integration (Direct Python)             │  │
│  │                                                          │  │
│  │  @st.cache_resource                                     │  │
│  │  - RecommendationEngine (loaded once)                   │  │
│  │  - Database connection (cached)                         │  │
│  │                                                          │  │
│  │  @st.cache_data                                         │  │
│  │  - Available cuisines                                   │  │
│  │  - Available locations                                  │  │
│  │  - Database statistics                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              RECOMMENDATION ENGINE (Phase 5)                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  RecommendationEngine                                   │  │
│  │  - get_recommendations(preferences)                     │  │
│  │  - get_available_cuisines()                             │  │
│  │  - get_available_locations()                            │  │
│  │  - get_database_stats()                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         ↓                 ↓                 ↓                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Database    │  │ Preference   │  │ LLM Service  │          │
│  │ Service     │  │ Processor    │  │              │          │
│  │ (Phase 1)   │  │ (Phase 3)    │  │ (Phase 4)    │          │
│  │             │  │              │  │              │          │
│  │ - Query     │  │ - Validate   │  │ - Generate   │          │
│  │ - Filter    │  │ - Normalize  │  │   explanations          │
│  │ - Enrich    │  │ - Summarize  │  │ - Support    │          │
│  │             │  │              │  │   Groq &     │          │
│  │             │  │              │  │   OpenRouter │          │
│  └─────────────┘  └──────────────┘  └──────────────┘          │
│         │                                    │                 │
│         └────────────────┬───────────────────┘                 │
│                          ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Data Processing Pipeline                              │  │
│  │  - Filter by cuisine                                   │  │
│  │  - Filter by location                                  │  │
│  │  - Filter by rating                                    │  │
│  │  - Filter by price                                     │  │
│  │  - Sort by relevance                                   │  │
│  │  - Limit results                                       │  │
│  │  - Enrich with explanations                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SQLite Database (restaurant.db)                        │  │
│  │                                                          │  │
│  │  Tables:                                                │  │
│  │  - restaurants (9,216+ records)                         │  │
│  │    * id, name, cuisine, location                        │  │
│  │    * rating, price, description                         │  │
│  │                                                          │  │
│  │  Statistics:                                            │  │
│  │  - 85 unique cuisines                                   │  │
│  │  - 92 unique locations                                  │  │
│  │  - Rating range: 0-5 stars                              │  │
│  │  - Price range: 1-5                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                              │
│                                                                 │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │  Groq API            │      │  OpenRouter API      │        │
│  │  (Free & Fast)       │      │  (Premium & Flexible)│        │
│  │                      │      │                      │        │
│  │  - mixtral-8x7b      │      │  - Multiple models   │        │
│  │  - Fast responses    │      │  - Custom routing    │        │
│  │  - Free tier         │      │  - Advanced features │        │
│  └──────────────────────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Submits Preferences

```
User Input (Streamlit Form)
    ↓
{
  "cuisine": ["Italian", "French"],
  "location": ["Downtown", "Midtown"],
  "min_rating": 3.5,
  "max_price": 4,
  "limit": 5
}
    ↓
Preference Processor (Phase 3)
    ↓
Validated & Normalized Preferences
```

### 2. Recommendation Engine Processes

```
Validated Preferences
    ↓
Database Service (Phase 1)
    ├─ Query restaurants
    ├─ Filter by cuisine
    ├─ Filter by location
    ├─ Filter by rating
    ├─ Filter by price
    └─ Sort & limit
    ↓
Filtered Restaurant List
    ↓
LLM Service (Phase 4)
    ├─ For each restaurant:
    │  ├─ Generate explanation
    │  ├─ Call Groq/OpenRouter API
    │  └─ Enrich with AI text
    ↓
Enriched Recommendations
```

### 3. Results Displayed

```
Enriched Recommendations
    ↓
Streamlit UI
    ├─ Restaurant cards
    ├─ Ratings & prices
    ├─ AI explanations
    └─ Filter summary
    ↓
User Views Results
```

---

## Component Architecture

### Phase 1: Data Pipeline
```
Input: Restaurant data (CSV/JSON)
    ↓
Ingestion (ingestion.py)
    ├─ Download from HuggingFace
    ├─ Parse data
    └─ Validate structure
    ↓
Preprocessing (preprocessing.py)
    ├─ Clean data
    ├─ Normalize values
    ├─ Handle missing data
    └─ Enrich records
    ↓
Storage (store.py)
    ├─ Create SQLite database
    ├─ Define schema
    └─ Insert records
    ↓
Output: restaurant.db (9,216+ restaurants)
```

### Phase 2: Recommendation API (Optional)
```
FastAPI Server (Port 8000)
    ├─ GET /health
    ├─ POST /api/v1/recommendations
    ├─ GET /api/v1/restaurants
    └─ GET /api/v1/stats
    ↓
Used by: React frontend (deprecated) or external clients
```

### Phase 3: Preference Processing
```
Input: User preferences (dict)
    ↓
validate_preferences()
    ├─ Check required fields
    ├─ Validate data types
    ├─ Normalize values
    └─ Apply defaults
    ↓
apply_defaults()
    ├─ Set default min_rating
    ├─ Set default max_price
    └─ Set default limit
    ↓
get_filter_summary()
    ├─ Create human-readable summary
    └─ Format for display
    ↓
Output: Validated preferences + summary
```

### Phase 4: LLM Integration
```
Input: Restaurant data
    ↓
Config (config.py)
    ├─ Load provider selection
    ├─ Load API keys
    └─ Set model parameters
    ↓
LLM Service (llm_service.py)
    ├─ Initialize client (Groq/OpenRouter)
    ├─ Call API
    └─ Handle responses
    ↓
Prompt Builder (prompt_builder.py)
    ├─ Create system prompt
    ├─ Create user prompt
    └─ Format for LLM
    ↓
Output: AI-generated explanations
```

### Phase 5: Recommendation Engine
```
Input: Validated preferences
    ↓
RecommendationEngine
    ├─ Initialize with database
    ├─ Load LLM service
    └─ Load preference processor
    ↓
get_recommendations()
    ├─ Query database
    ├─ Apply filters
    ├─ Sort results
    ├─ Enrich with LLM
    └─ Return results
    ↓
Output: List of restaurants with explanations
```

### Phase 6: Frontend (Deprecated - Replaced by Streamlit)
```
React App (Port 5173)
    ├─ PreferenceForm component
    ├─ ResultsSection component
    ├─ LoadingState component
    └─ ErrorMessage component
    ↓
API Service (api.js)
    ├─ Call /api/v1/recommendations
    ├─ Handle responses
    └─ Manage errors
    ↓
FastAPI Backend (Port 8000)
```

---

## Deployment Architecture

### Streamlit Cloud
```
GitHub Repository
    ↓
Streamlit Cloud
    ├─ Clone repo
    ├─ Install dependencies
    ├─ Run streamlit_app.py
    └─ Expose on streamlit.app domain
    ↓
User Browser
    ├─ Access app
    ├─ Submit preferences
    └─ View recommendations
```

### Docker
```
Dockerfile
    ↓
Docker Build
    ├─ Base: python:3.11-slim
    ├─ Install dependencies
    ├─ Copy code
    └─ Expose port 8501
    ↓
Docker Container
    ├─ Run streamlit_app.py
    ├─ Mount database volume
    └─ Set environment variables
    ↓
User Access
    ├─ localhost:8501
    ├─ or domain:8501
    └─ or load balancer
```

### Traditional Server
```
Server (AWS/DigitalOcean/etc)
    ├─ Clone repository
    ├─ Install Python 3.11+
    ├─ Create virtual environment
    ├─ Install dependencies
    └─ Run streamlit_app.py
    ↓
Process Manager (systemd/supervisor)
    ├─ Monitor process
    ├─ Auto-restart on failure
    └─ Manage logs
    ↓
Reverse Proxy (nginx/Apache)
    ├─ Handle HTTPS
    ├─ Load balance
    └─ Cache static files
    ↓
User Access
    ├─ domain.com
    └─ Automatic HTTPS
```

---

## Caching Strategy

### Streamlit Caching

```
@st.cache_resource
def load_engine():
    """Load once per session"""
    return RecommendationEngine()
    
    Lifetime: Session
    Scope: Across reruns
    Use: Expensive initialization
```

```
@st.cache_data
def get_available_options():
    """Cache database queries"""
    return cuisines, locations
    
    Lifetime: Until data changes
    Scope: Across sessions
    Use: Static data
```

### Performance Impact

```
First Load:
  - Load engine: 10-30 seconds
  - Query database: 1-2 seconds
  - Total: 10-30 seconds

Subsequent Loads:
  - Load engine: <100ms (cached)
  - Query database: <100ms (cached)
  - Total: <1 second

Recommendation Request:
  - Filter restaurants: 1-2 seconds
  - Call LLM API: 2-5 seconds
  - Total: 3-7 seconds
```

---

## Security Architecture

```
User Input
    ↓
Streamlit Input Validation
    ├─ Type checking
    ├─ Range validation
    └─ Sanitization
    ↓
Preference Processor
    ├─ Normalize values
    ├─ Check constraints
    └─ Apply defaults
    ↓
Database Query
    ├─ Parameterized queries
    ├─ No SQL injection
    └─ Read-only access
    ↓
LLM API Call
    ├─ API key from environment
    ├─ HTTPS connection
    └─ Rate limiting
    ↓
Response to User
    ├─ Sanitize output
    ├─ Error handling
    └─ No sensitive data
```

---

## Scalability Considerations

### Current Limitations
- SQLite: Single-file database (not ideal for concurrent writes)
- Streamlit: Single-threaded (one request at a time)
- LLM API: Rate limits depend on provider

### Scaling Solutions

**Database**
```
SQLite (Development)
    ↓
PostgreSQL (Production)
    ├─ Multi-user support
    ├─ Better concurrency
    └─ Advanced features
```

**Application**
```
Single Streamlit Instance
    ↓
Multiple Instances + Load Balancer
    ├─ Horizontal scaling
    ├─ High availability
    └─ Better performance
```

**LLM**
```
Single Provider
    ↓
Multiple Providers
    ├─ Fallback support
    ├─ Load balancing
    └─ Cost optimization
```

---

## Monitoring & Logging

```
Streamlit Application
    ├─ Application logs
    │  ├─ User actions
    │  ├─ Errors
    │  └─ Performance metrics
    │
    ├─ Database logs
    │  ├─ Query performance
    │  ├─ Connection issues
    │  └─ Data integrity
    │
    └─ LLM logs
       ├─ API calls
       ├─ Response times
       └─ Error rates
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Web UI |
| **Backend** | Python | Business logic |
| **Database** | SQLite | Data storage |
| **LLM** | Groq/OpenRouter | AI explanations |
| **Deployment** | Docker | Containerization |
| **Server** | Streamlit Cloud/Traditional | Hosting |

---

## File Organization

```
streamlit_app.py
    ├─ Imports
    ├─ Configuration
    ├─ Caching functions
    ├─ Main UI components
    └─ Main function

restaurant-recommendation/
├── phase-1-data-pipeline/
│   ├─ src/data/
│   │  ├─ ingestion.py
│   │  ├─ preprocessing.py
│   │  └─ store.py
│   └─ data/restaurant.db
│
├── phase-3-preference-processing/
│   └─ src/preference_processor.py
│
├── phase-4-llm-integration/
│   └─ src/
│      ├─ llm_service.py
│      ├─ prompt_builder.py
│      └─ config.py
│
└── phase-5-recommendation-engine/
    └─ src/
       ├─ recommendation_engine.py
       ├─ database_service.py
       └─ config.py
```

---

This architecture provides a scalable, maintainable, and performant system for restaurant recommendations with AI-powered explanations.

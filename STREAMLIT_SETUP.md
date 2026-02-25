# Streamlit Setup & Deployment Guide

## Overview

The Restaurant Recommendation Engine is now ready for Streamlit deployment. This guide covers local setup, testing, and production deployment.

## Files Created

- `streamlit_app.py` - Main Streamlit application
- `.streamlit/config.toml` - Streamlit configuration
- `requirements-streamlit.txt` - Python dependencies
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Docker Compose orchestration
- `run_streamlit.sh` - Linux/Mac startup script
- `run_streamlit.bat` - Windows startup script
- `STREAMLIT_DEPLOYMENT.md` - Detailed deployment guide

## Quick Start (Local Development)

### Windows
```bash
run_streamlit.bat
```

### Linux/Mac
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements-streamlit.txt

# Run the app
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

## Configuration

### 1. Environment Variables

Copy `.env.streamlit.example` to `.env` in each phase directory:

```bash
# Phase 2 (API)
cp restaurant-recommendation/phase-2-recommendation-api/.env.example restaurant-recommendation/phase-2-recommendation-api/.env

# Phase 4 (LLM)
cp restaurant-recommendation/phase-4-llm-integration/.env.example restaurant-recommendation/phase-4-llm-integration/.env

# Phase 5 (Engine)
cp restaurant-recommendation/phase-5-recommendation-engine/.env.example restaurant-recommendation/phase-5-recommendation-engine/.env
```

### 2. LLM Provider Setup

Choose your LLM provider:

#### Option A: Groq (Recommended - Free & Fast)
1. Sign up at https://console.groq.com
2. Get your API key
3. Set in `.env`:
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_key_here
   ```

#### Option B: OpenRouter (Premium & Flexible)
1. Sign up at https://openrouter.ai
2. Get your API key
3. Set in `.env`:
   ```
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your_key_here
   ```

### 3. Database

The SQLite database is located at:
```
restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db
```

If the database doesn't exist, run the data pipeline first:
```bash
cd restaurant-recommendation/phase-1-data-pipeline
python load_full_dataset.py
```

## Deployment Options

### Option 1: Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your repo and `streamlit_app.py`
5. Add secrets in app settings:
   ```
   GROQ_API_KEY = "your_key"
   ```

**Pros**: Free tier available, automatic HTTPS, easy updates
**Cons**: Limited resources, requires GitHub

### Option 2: Docker (Recommended for Production)

```bash
# Build image
docker build -t restaurant-recommender .

# Run container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  restaurant-recommender
```

Or with Docker Compose:
```bash
# Create .env file with your API keys
echo "GROQ_API_KEY=your_key" > .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f streamlit

# Stop services
docker-compose down
```

**Pros**: Consistent environment, easy scaling, production-ready
**Cons**: Requires Docker knowledge

### Option 3: Traditional Server (AWS, DigitalOcean, etc.)

1. SSH into server
2. Clone repository
3. Install Python 3.11+
4. Set up virtual environment
5. Install dependencies
6. Configure systemd service (see STREAMLIT_DEPLOYMENT.md)
7. Start service

**Pros**: Full control, scalable, cost-effective
**Cons**: More setup required

### Option 4: Heroku (Simple Cloud Deployment)

1. Create `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.7
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set GROQ_API_KEY=your_key
   git push heroku main
   ```

**Pros**: Simple deployment, free tier available
**Cons**: Limited resources, slower cold starts

## Features

### User Interface
- 🔍 **Smart Search**: Filter by cuisine, location, rating, and price
- ⭐ **Ratings & Reviews**: See restaurant ratings and prices
- 💡 **AI Explanations**: Get AI-powered reasons for recommendations
- 📊 **Database Stats**: View database information in sidebar
- 🎨 **Modern Design**: Clean, responsive interface

### Backend
- ⚡ **Fast**: Direct engine integration, no HTTP overhead
- 🔄 **Cached**: Automatic caching of engine and queries
- 🤖 **AI-Powered**: LLM explanations for each recommendation
- ✅ **Validated**: Input validation and preference normalization

## Troubleshooting

### App won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep streamlit

# Run with debug
streamlit run streamlit_app.py --logger.level=debug
```

### Database not found
```bash
# Check database exists
ls restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db

# If missing, load data
cd restaurant-recommendation/phase-1-data-pipeline
python load_full_dataset.py
```

### LLM not working
```bash
# Check API key is set
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows

# Test API key
python -c "from groq import Groq; print('OK')"
```

### Slow performance
- First load caches engine (10-30 seconds)
- Subsequent loads are instant
- Check system resources (CPU, RAM)

## Performance Tips

1. **Caching**: Engine is cached after first load
2. **Database**: Queries are cached automatically
3. **Lazy Loading**: Stats only load when needed
4. **Session State**: Form inputs persist

## Security

1. **API Keys**: Use environment variables, never hardcode
2. **Database**: SQLite for dev, PostgreSQL for production
3. **Input Validation**: All inputs validated before processing
4. **Error Handling**: Sensitive errors hidden from users

## Monitoring

### Local Development
```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Production
- Streamlit Cloud: Built-in analytics
- Docker: Check logs with `docker logs`
- Server: Use systemd journal or log files

## Next Steps

1. ✅ Test locally
2. ✅ Configure LLM provider
3. ✅ Choose deployment platform
4. ✅ Deploy application
5. ✅ Monitor and iterate

## Support

- Streamlit Docs: https://docs.streamlit.io
- Groq Docs: https://console.groq.com/docs
- OpenRouter Docs: https://openrouter.ai/docs
- Project Issues: Check phase-specific READMEs

## Architecture

```
┌─────────────────────────────────────┐
│     Streamlit Web Interface         │
│  (streamlit_app.py)                 │
└──────────────┬──────────────────────┘
               │
               ├─→ RecommendationEngine (Phase 5)
               │   ├─→ DatabaseService (Phase 1)
               │   └─→ LLMService (Phase 4)
               │
               ├─→ PreferenceProcessor (Phase 3)
               │
               └─→ SQLite Database
                   (restaurant.db)
```

## What's Different from React Frontend?

| Aspect | React | Streamlit |
|--------|-------|-----------|
| Framework | React 18 + Vite | Streamlit |
| Deployment | Separate frontend/backend | Single app |
| Performance | HTTP calls | Direct integration |
| Development | Complex build process | Simple Python |
| Hosting | Vercel, Netlify, etc. | Streamlit Cloud, Docker |
| Styling | Tailwind CSS | Streamlit components |

## Keeping Both Frontends

You can keep both React and Streamlit:
- React: For advanced users, custom integrations
- Streamlit: For quick deployment, data exploration

Just ensure the FastAPI backend is running:
```bash
cd restaurant-recommendation/phase-2-recommendation-api
python start_api.py
```

Then run Streamlit in another terminal:
```bash
streamlit run streamlit_app.py
```

---

**Ready to deploy? Start with `run_streamlit.bat` (Windows) or `./run_streamlit.sh` (Linux/Mac)!**

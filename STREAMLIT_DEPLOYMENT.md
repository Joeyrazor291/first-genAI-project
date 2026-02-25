# Streamlit Deployment Guide

This guide explains how to deploy the Restaurant Recommendation Engine on Streamlit.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-streamlit.txt
```

### 2. Configure Environment

Ensure your `.env` files are properly set up in each phase directory:

- `restaurant-recommendation/phase-2-recommendation-api/.env`
- `restaurant-recommendation/phase-4-llm-integration/.env`
- `restaurant-recommendation/phase-5-recommendation-engine/.env`

For LLM integration, set your provider:
```
LLM_PROVIDER=groq  # or openrouter
GROQ_API_KEY=your_key_here
# or
OPENROUTER_API_KEY=your_key_here
```

### 3. Run Locally

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Quick Deployment)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and `streamlit_app.py`
5. Add secrets in the Streamlit Cloud dashboard:
   - Go to App settings → Secrets
   - Add your LLM API keys:
     ```
     GROQ_API_KEY = "your_key"
     # or
     OPENROUTER_API_KEY = "your_key"
     ```

### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-streamlit.txt .
RUN pip install -r requirements-streamlit.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t restaurant-recommender .
docker run -p 8501:8501 restaurant-recommender
```

### Option 3: Traditional Server Deployment (AWS, DigitalOcean, etc.)

1. SSH into your server
2. Clone the repository
3. Install Python 3.11+
4. Install dependencies: `pip install -r requirements-streamlit.txt`
5. Set up environment variables
6. Run with a process manager (systemd, supervisor, etc.)

Example systemd service (`/etc/systemd/system/streamlit-app.service`):
```ini
[Unit]
Description=Restaurant Recommendation Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 -m streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app
```

### Option 4: Heroku Deployment

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

## Features

### User Interface
- **Preference Form**: Select cuisines, locations, rating range, and price range
- **Real-time Results**: Get restaurant recommendations with AI explanations
- **Database Statistics**: View database info in the sidebar
- **Filter Summary**: See what filters were applied
- **Expandable Details**: Click to see AI-generated explanations

### Backend Integration
- Direct integration with RecommendationEngine (no HTTP overhead)
- Automatic caching of engine and database queries
- LLM-powered explanations for each recommendation
- Preference validation and normalization

## Configuration

### Streamlit Settings (`.streamlit/config.toml`)
- Theme customization
- Server port (default: 8501)
- Client settings
- Logger configuration

### Environment Variables
Set in `.env` files or Streamlit Cloud secrets:
- `LLM_PROVIDER`: "groq" or "openrouter"
- `GROQ_API_KEY`: Your Groq API key
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `DATABASE_PATH`: Path to SQLite database

## Troubleshooting

### Database Connection Issues
- Ensure `restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db` exists
- Check file permissions
- Verify the database path in the code

### LLM Integration Not Working
- Verify API keys are set correctly
- Check that the LLM provider is configured
- Look at Streamlit logs for error messages

### Slow Performance
- The first load caches the engine (may take 10-30 seconds)
- Subsequent loads are instant
- Database queries are cached automatically

### Import Errors
- Ensure all phase directories are in the Python path
- Check that all dependencies are installed
- Verify the directory structure matches the code

## Performance Optimization

1. **Caching**: Engine and database queries are cached with `@st.cache_resource` and `@st.cache_data`
2. **Direct Integration**: No HTTP overhead compared to calling the API
3. **Lazy Loading**: Database stats only load when needed
4. **Session State**: Form inputs persist across reruns

## Security Considerations

1. **API Keys**: Use Streamlit Cloud secrets or environment variables, never hardcode
2. **Database**: SQLite is file-based; for production, consider PostgreSQL
3. **Input Validation**: All user inputs are validated before processing
4. **Error Handling**: Sensitive errors are caught and user-friendly messages shown

## Monitoring

### Streamlit Cloud
- Built-in app analytics and logs
- Monitor app health and performance
- View user sessions

### Self-Hosted
- Check application logs: `streamlit run streamlit_app.py --logger.level=debug`
- Monitor system resources (CPU, memory)
- Set up log aggregation (ELK, Datadog, etc.)

## Next Steps

1. Test locally: `streamlit run streamlit_app.py`
2. Deploy to Streamlit Cloud for quick testing
3. Set up production deployment with your preferred platform
4. Configure monitoring and alerting
5. Gather user feedback and iterate

## Support

For issues or questions:
- Check Streamlit documentation: https://docs.streamlit.io
- Review phase-specific READMEs in each phase directory
- Check LLM provider documentation (Groq, OpenRouter)

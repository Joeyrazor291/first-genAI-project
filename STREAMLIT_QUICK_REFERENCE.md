# Streamlit Deployment - Quick Reference

## 🚀 Start Here

### Windows
```bash
run_streamlit.bat
```

### Linux/Mac
```bash
./run_streamlit.sh
```

### Manual
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

**App opens at**: http://localhost:8501

---

## 📋 Pre-Deployment Checklist

- [ ] Database exists: `restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db`
- [ ] `.env` files configured in each phase directory
- [ ] LLM API key set (Groq or OpenRouter)
- [ ] Python 3.11+ installed
- [ ] All dependencies installed: `pip install -r requirements-streamlit.txt`
- [ ] App runs locally without errors

---

## 🌐 Deployment Platforms

### Streamlit Cloud (Easiest)
```bash
git push origin main
# Go to https://share.streamlit.io → New app
# Add secrets in app settings
```

### Docker
```bash
docker build -t restaurant-recommender .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key restaurant-recommender
```

### Docker Compose
```bash
docker-compose up -d
```

### Traditional Server
```bash
# SSH into server
git clone <repo>
cd <repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
```

---

## 🔧 Configuration

### LLM Provider (Choose One)

**Groq (Free & Fast)**
```
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
```

**OpenRouter (Premium)**
```
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
```

### Environment Variables
Set in `.env` files or Streamlit Cloud secrets:
- `LLM_PROVIDER` - Which LLM to use
- `GROQ_API_KEY` - Groq API key
- `OPENROUTER_API_KEY` - OpenRouter API key
- `DATABASE_PATH` - Path to SQLite database

---

## 📁 Project Structure

```
.
├── streamlit_app.py                    # Main Streamlit app
├── .streamlit/config.toml              # Streamlit config
├── requirements-streamlit.txt          # Dependencies
├── Dockerfile                          # Docker image
├── docker-compose.yml                  # Docker Compose
├── run_streamlit.sh                    # Linux/Mac startup
├── run_streamlit.bat                   # Windows startup
├── STREAMLIT_SETUP.md                  # Setup guide
├── STREAMLIT_DEPLOYMENT.md             # Deployment guide
└── restaurant-recommendation/
    ├── phase-1-data-pipeline/          # Database
    ├── phase-2-recommendation-api/     # API (optional)
    ├── phase-3-preference-processing/  # Validation
    ├── phase-4-llm-integration/        # LLM service
    ├── phase-5-recommendation-engine/  # Core engine
    └── phase-6-frontend/               # React (deprecated)
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements-streamlit.txt` |
| Database not found | Run `cd restaurant-recommendation/phase-1-data-pipeline && python load_full_dataset.py` |
| LLM not working | Check API key is set and valid |
| Port 8501 in use | `streamlit run streamlit_app.py --server.port=8502` |
| Slow first load | Normal - engine caches on first run (10-30s) |

---

## 📊 Features

✅ Search by cuisine, location, rating, price
✅ AI-powered explanations for recommendations
✅ Database statistics in sidebar
✅ Real-time filtering and results
✅ Responsive design
✅ Fast performance with caching

---

## 🔐 Security Tips

1. Never hardcode API keys
2. Use environment variables or Streamlit secrets
3. For production, use PostgreSQL instead of SQLite
4. Enable HTTPS (automatic on Streamlit Cloud)
5. Validate all user inputs (already done)

---

## 📈 Performance

- **First load**: 10-30 seconds (engine caching)
- **Subsequent loads**: <1 second
- **Database queries**: Cached automatically
- **Concurrent users**: Depends on deployment platform

---

## 🎯 Next Steps

1. **Local Testing**: Run `streamlit run streamlit_app.py`
2. **Configure LLM**: Set up Groq or OpenRouter API key
3. **Choose Platform**: Streamlit Cloud, Docker, or traditional server
4. **Deploy**: Follow platform-specific instructions
5. **Monitor**: Check logs and user feedback

---

## 📚 Documentation

- **Setup Guide**: `STREAMLIT_SETUP.md`
- **Deployment Guide**: `STREAMLIT_DEPLOYMENT.md`
- **Streamlit Docs**: https://docs.streamlit.io
- **Groq Docs**: https://console.groq.com/docs
- **OpenRouter Docs**: https://openrouter.ai/docs

---

## 💡 Tips

- Use `@st.cache_resource` for expensive operations
- Use `@st.cache_data` for database queries
- Use `st.spinner()` for loading states
- Use `st.error()` and `st.warning()` for messages
- Test locally before deploying

---

## 🆘 Getting Help

1. Check the troubleshooting section above
2. Review phase-specific READMEs
3. Check Streamlit documentation
4. Review LLM provider documentation
5. Check application logs with `--logger.level=debug`

---

**Happy deploying! 🎉**

# Streamlit Troubleshooting Guide

## Common Issues & Solutions

### 1. Import Errors

#### Error: `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install -r requirements-streamlit.txt
```

Or install Streamlit directly:
```bash
pip install streamlit>=1.28.0
```

---

#### Error: `ModuleNotFoundError: No module named 'recommendation_engine'`

**Solution:**
The app adds phase directories to Python path. Ensure they exist:
```bash
# Check these directories exist:
ls restaurant-recommendation/phase-1-data-pipeline/src
ls restaurant-recommendation/phase-3-preference-processing/src
ls restaurant-recommendation/phase-4-llm-integration/src
ls restaurant-recommendation/phase-5-recommendation-engine/src
```

If missing, run the data pipeline first:
```bash
cd restaurant-recommendation/phase-1-data-pipeline
python load_full_dataset.py
```

---

### 2. Database Issues

#### Error: `FileNotFoundError: restaurant.db not found`

**Solution:**
The database needs to be created. Run the data pipeline:
```bash
cd restaurant-recommendation/phase-1-data-pipeline
python load_full_dataset.py
```

This will:
- Download restaurant data
- Process and clean it
- Create SQLite database
- Populate with 9,216+ restaurants

**Time**: ~5-10 minutes depending on internet speed

---

#### Error: `sqlite3.DatabaseError: database disk image is malformed`

**Solution:**
The database file is corrupted. Recreate it:
```bash
# Remove corrupted database
rm restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db

# Recreate it
cd restaurant-recommendation/phase-1-data-pipeline
python load_full_dataset.py
```

---

#### Error: `OperationalError: no such table: restaurants`

**Solution:**
Database exists but is empty. Populate it:
```bash
cd restaurant-recommendation/phase-1-data-pipeline
python load_full_dataset.py
```

---

### 3. LLM Integration Issues

#### Error: `groq.error.AuthenticationError: Invalid API key`

**Solution:**
1. Verify API key is correct:
   ```bash
   # Linux/Mac
   echo $GROQ_API_KEY
   
   # Windows
   echo %GROQ_API_KEY%
   ```

2. Check `.env` file:
   ```bash
   cat restaurant-recommendation/phase-4-llm-integration/.env
   ```

3. Get a new API key:
   - Go to https://console.groq.com
   - Create new API key
   - Update `.env` file

---

#### Error: `openai.error.AuthenticationError: Invalid API key`

**Solution:**
1. Verify OpenRouter API key:
   ```bash
   echo $OPENROUTER_API_KEY
   ```

2. Check `.env` file has correct provider:
   ```
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your_key
   ```

3. Get new key from https://openrouter.ai

---

#### Error: `LLM service not responding` or `Timeout`

**Solution:**
1. Check internet connection
2. Verify API key is valid
3. Check API rate limits
4. Try a different LLM provider
5. Disable LLM temporarily:
   ```python
   # In streamlit_app.py, comment out explanation section
   ```

---

### 4. Port Issues

#### Error: `Address already in use: ('0.0.0.0', 8501)`

**Solution:**
Use a different port:
```bash
streamlit run streamlit_app.py --server.port=8502
```

Or kill the process using port 8501:
```bash
# Linux/Mac
lsof -i :8501
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

### 5. Performance Issues

#### Problem: App is slow on first load

**Expected behavior**: First load takes 10-30 seconds (engine caching)

**Solution:**
- This is normal
- Subsequent loads are instant
- Use `st.spinner()` to show loading state (already done)

---

#### Problem: Recommendations take too long

**Solution:**
1. Check database size:
   ```bash
   ls -lh restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db
   ```

2. Check system resources:
   ```bash
   # Linux/Mac
   top
   
   # Windows
   tasklist
   ```

3. Reduce recommendation limit in UI

4. Check LLM provider response time

---

### 6. Environment Variable Issues

#### Error: `KeyError: 'LLM_PROVIDER'` or similar

**Solution:**
1. Create `.env` files in each phase:
   ```bash
   cp restaurant-recommendation/phase-2-recommendation-api/.env.example \
      restaurant-recommendation/phase-2-recommendation-api/.env
   
   cp restaurant-recommendation/phase-4-llm-integration/.env.example \
      restaurant-recommendation/phase-4-llm-integration/.env
   ```

2. Edit `.env` files with your settings

3. Verify they're loaded:
   ```bash
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('LLM_PROVIDER'))"
   ```

---

### 7. Docker Issues

#### Error: `docker: command not found`

**Solution:**
Install Docker:
- **Windows/Mac**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- **Linux**: `sudo apt-get install docker.io`

---

#### Error: `docker: permission denied`

**Solution:**
Add user to docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

#### Error: `docker-compose: command not found`

**Solution:**
Install Docker Compose:
```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Mac/Windows
# Already included with Docker Desktop
```

---

#### Error: `Container exits immediately`

**Solution:**
Check logs:
```bash
docker logs restaurant-recommender
```

Common causes:
- Missing environment variables
- Database not found
- Port already in use

---

### 8. Streamlit Cloud Issues

#### Error: `ModuleNotFoundError` on Streamlit Cloud

**Solution:**
1. Ensure `requirements-streamlit.txt` is in repo root
2. Commit and push to GitHub
3. Redeploy from Streamlit Cloud

---

#### Error: `Secret not found` on Streamlit Cloud

**Solution:**
1. Go to app settings
2. Click "Secrets"
3. Add your secrets:
   ```
   GROQ_API_KEY = "your_key"
   ```

4. Redeploy app

---

### 9. Virtual Environment Issues

#### Error: `venv: command not found`

**Solution:**
```bash
# Linux/Mac
python3 -m venv venv

# Windows
python -m venv venv
```

---

#### Error: `activate: command not found`

**Solution:**
Use correct activation command:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### 10. Dependency Issues

#### Error: `pip: command not found`

**Solution:**
```bash
# Linux/Mac
python3 -m pip install -r requirements-streamlit.txt

# Windows
python -m pip install -r requirements-streamlit.txt
```

---

#### Error: `Conflicting dependencies`

**Solution:**
Create fresh virtual environment:
```bash
# Remove old one
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Create new one
python -m venv venv

# Activate and install
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

pip install -r requirements-streamlit.txt
```

---

## Debugging Tips

### Enable Debug Logging

```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Check Configuration

```bash
python -c "
import streamlit as st
print('Streamlit version:', st.__version__)
print('Python version:', __import__('sys').version)
"
```

### Test Database Connection

```bash
python -c "
import sqlite3
db = sqlite3.connect('restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db')
cursor = db.cursor()
cursor.execute('SELECT COUNT(*) FROM restaurants')
print('Total restaurants:', cursor.fetchone()[0])
"
```

### Test LLM Connection

```bash
python -c "
from groq import Groq
import os
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
response = client.chat.completions.create(
    model='mixtral-8x7b-32768',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print('LLM working:', response.choices[0].message.content[:50])
"
```

---

## Performance Optimization

### Reduce Initial Load Time

1. **Cache engine**:
   ```python
   @st.cache_resource
   def load_engine():
       return RecommendationEngine()
   ```

2. **Cache database queries**:
   ```python
   @st.cache_data
   def get_available_options():
       return engine.get_available_cuisines(), engine.get_available_locations()
   ```

3. **Lazy load stats**:
   ```python
   if st.sidebar.checkbox("Show Stats"):
       # Load stats only if requested
   ```

---

## Getting Help

1. **Check logs**:
   ```bash
   streamlit run streamlit_app.py --logger.level=debug 2>&1 | tee app.log
   ```

2. **Review documentation**:
   - `STREAMLIT_SETUP.md`
   - `STREAMLIT_DEPLOYMENT.md`
   - Phase-specific READMEs

3. **Check external resources**:
   - Streamlit: https://docs.streamlit.io
   - Groq: https://console.groq.com/docs
   - OpenRouter: https://openrouter.ai/docs

4. **Test components individually**:
   ```bash
   # Test database
   python restaurant-recommendation/phase-1-data-pipeline/tests/test_store.py
   
   # Test engine
   python restaurant-recommendation/phase-5-recommendation-engine/tests/test_engine.py
   ```

---

## Quick Fixes Checklist

- [ ] Run `pip install -r requirements-streamlit.txt`
- [ ] Check database exists: `ls restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db`
- [ ] Verify `.env` files are configured
- [ ] Check API keys are valid
- [ ] Try different port: `streamlit run streamlit_app.py --server.port=8502`
- [ ] Clear cache: `rm -rf ~/.streamlit/cache`
- [ ] Restart terminal/IDE
- [ ] Check Python version: `python --version` (should be 3.11+)
- [ ] Try fresh virtual environment
- [ ] Check internet connection

---

## Still Having Issues?

1. **Collect information**:
   - Error message (full traceback)
   - Python version
   - OS and platform
   - Steps to reproduce

2. **Check logs**:
   ```bash
   streamlit run streamlit_app.py --logger.level=debug
   ```

3. **Review phase-specific issues**:
   - Check `restaurant-recommendation/phase-*/README.md`
   - Check `restaurant-recommendation/phase-*/tests/`

4. **Test components**:
   - Test database connection
   - Test LLM connection
   - Test recommendation engine

---

**Remember**: Most issues are related to missing dependencies, incorrect configuration, or missing database. Start with the checklist above!

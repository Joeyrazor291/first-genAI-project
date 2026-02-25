# Streamlit Secrets Configuration Guide

## Overview

This guide explains how to configure LLM API keys and other sensitive information for the Streamlit application using TOML format.

## File Locations

### Local Development
```
.streamlit/secrets.toml
```

### Streamlit Cloud
Secrets are managed through the app settings dashboard (no file needed).

---

## TOML Configuration Format

### Basic Structure

```toml
# LLM Provider Configuration
llm_provider = "groq"  # or "openrouter"

# API Keys
groq_api_key = "your_key_here"
openrouter_api_key = "your_key_here"

# Database
database_path = "restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db"

# Server Settings
[server]
port = 8501
address = "0.0.0.0"
headless = true

# Logging
[logger]
level = "info"

# Theme
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
```

---

## Setup Instructions

### Option 1: Local Development with TOML

1. **Create/Edit `.streamlit/secrets.toml`**:
   ```bash
   # File already exists at .streamlit/secrets.toml
   # Edit it with your API keys
   ```

2. **Add your Groq API key**:
   ```toml
   llm_provider = "groq"
   groq_api_key = "gsk_your_actual_key_here"
   ```

3. **Or use OpenRouter**:
   ```toml
   llm_provider = "openrouter"
   openrouter_api_key = "sk-or-your_actual_key_here"
   ```

4. **Run Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

### Option 2: Streamlit Cloud

1. **Push code to GitHub** (without secrets.toml):
   ```bash
   git add -A
   git commit -m "Update Streamlit app"
   git push origin main
   ```

2. **Go to Streamlit Cloud**:
   - Visit https://share.streamlit.io
   - Click on your app
   - Go to "Settings" → "Secrets"

3. **Add secrets in TOML format**:
   ```toml
   llm_provider = "groq"
   groq_api_key = "gsk_your_actual_key_here"
   ```

4. **Save and redeploy**

---

## Complete TOML Configuration Examples

### Example 1: Using Groq (Recommended)

```toml
# LLM Provider Configuration
llm_provider = "groq"

# Groq API Key (get from https://console.groq.com)
groq_api_key = "gsk_your_actual_key_here"

# Database Configuration
database_path = "restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db"

# Server Configuration
[server]
port = 8501
address = "0.0.0.0"
headless = true
runOnSave = true

# Logging Configuration
[logger]
level = "info"

# Client Configuration
[client]
showErrorDetails = true
toolbarMode = "viewer"

# Theme Configuration
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Example 2: Using OpenRouter

```toml
# LLM Provider Configuration
llm_provider = "openrouter"

# OpenRouter API Key (get from https://openrouter.ai)
openrouter_api_key = "sk-or-your_actual_key_here"

# Database Configuration
database_path = "restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db"

# Server Configuration
[server]
port = 8501
address = "0.0.0.0"
headless = true

# Logging Configuration
[logger]
level = "info"

# Client Configuration
[client]
showErrorDetails = true
toolbarMode = "viewer"

# Theme Configuration
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Example 3: Production Configuration

```toml
# LLM Provider Configuration
llm_provider = "groq"
groq_api_key = "gsk_your_actual_key_here"

# Database Configuration
database_path = "/var/data/restaurant.db"

# Server Configuration
[server]
port = 8501
address = "0.0.0.0"
headless = true
runOnSave = false
maxUploadSize = 200

# Logging Configuration
[logger]
level = "warning"

# Client Configuration
[client]
showErrorDetails = false
toolbarMode = "minimal"

# Theme Configuration
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## Getting API Keys

### Groq (Free & Fast)

1. Go to https://console.groq.com
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)
6. Add to `secrets.toml`:
   ```toml
   groq_api_key = "gsk_your_key_here"
   ```

### OpenRouter (Premium & Flexible)

1. Go to https://openrouter.ai
2. Sign up or log in
3. Navigate to "Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-or-`)
6. Add to `secrets.toml`:
   ```toml
   openrouter_api_key = "sk-or-your_key_here"
   ```

---

## TOML Syntax Guide

### Basic Key-Value Pairs
```toml
# String
llm_provider = "groq"

# Number
port = 8501

# Boolean
headless = true

# Array
allowed_hosts = ["localhost", "127.0.0.1"]
```

### Sections (Tables)
```toml
[server]
port = 8501
address = "0.0.0.0"

[logger]
level = "info"

[theme]
primaryColor = "#FF6B35"
```

### Nested Sections
```toml
[database]
[database.connection]
host = "localhost"
port = 5432
```

---

## Security Best Practices

### ✅ DO:
- Store API keys in `.streamlit/secrets.toml` (local development)
- Use Streamlit Cloud secrets for production
- Never commit `secrets.toml` to GitHub
- Rotate API keys regularly
- Use environment-specific configurations

### ❌ DON'T:
- Hardcode API keys in Python files
- Commit `secrets.toml` to version control
- Share API keys in chat or email
- Use the same key for development and production
- Store secrets in plain text files outside `.streamlit/`

---

## .gitignore Configuration

Ensure `.streamlit/secrets.toml` is ignored by Git:

```bash
# Add to .gitignore
.streamlit/secrets.toml
```

Or create `.streamlit/.gitignore`:
```
secrets.toml
```

---

## Accessing Secrets in Python

### In Streamlit App

```python
import streamlit as st

# Access string value
llm_provider = st.secrets["llm_provider"]

# Access with default value
groq_key = st.secrets.get("groq_api_key", "")

# Access nested value
port = st.secrets["server"]["port"]

# Check if key exists
if "groq_api_key" in st.secrets:
    print("Groq key found")
```

### In Regular Python Scripts

```python
import toml

# Load secrets
with open(".streamlit/secrets.toml", "r") as f:
    secrets = toml.load(f)

llm_provider = secrets["llm_provider"]
groq_key = secrets.get("groq_api_key", "")
```

---

## Troubleshooting

### Issue: "Secret not found" error

**Solution**:
1. Check `.streamlit/secrets.toml` exists
2. Verify key name is correct
3. Check TOML syntax is valid
4. Restart Streamlit: `streamlit run streamlit_app.py`

### Issue: API key not working

**Solution**:
1. Verify key is correct (copy-paste carefully)
2. Check key hasn't expired
3. Verify key has correct permissions
4. Test key with provider's API directly

### Issue: TOML parsing error

**Solution**:
1. Check TOML syntax (use https://www.toml-lint.com/)
2. Ensure quotes are correct
3. Check for special characters
4. Validate indentation

### Issue: Secrets work locally but not on Streamlit Cloud

**Solution**:
1. Add secrets to Streamlit Cloud app settings
2. Use same key names as local `secrets.toml`
3. Redeploy app after adding secrets
4. Check app logs for errors

---

## Environment Variable Mapping

The Streamlit app automatically maps TOML secrets to environment variables:

| TOML Key | Environment Variable |
|----------|----------------------|
| `llm_provider` | `LLM_PROVIDER` |
| `groq_api_key` | `GROQ_API_KEY` |
| `openrouter_api_key` | `OPENROUTER_API_KEY` |
| `database_path` | `DATABASE_PATH` |

---

## Streamlit Cloud Setup

### Step-by-Step

1. **Push code to GitHub**:
   ```bash
   git add -A
   git commit -m "Update Streamlit configuration"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository and `streamlit_app.py`

3. **Add Secrets**:
   - Click on app settings (gear icon)
   - Select "Secrets"
   - Add your secrets in TOML format:
     ```toml
     llm_provider = "groq"
     groq_api_key = "gsk_your_actual_key_here"
     ```
   - Click "Save"

4. **Redeploy**:
   - App automatically redeploys with new secrets

---

## Docker Configuration

### Using Secrets with Docker

Create a `.env` file for Docker:
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here
```

Run Docker with environment variables:
```bash
docker run -p 8501:8501 \
  -e LLM_PROVIDER=groq \
  -e GROQ_API_KEY=gsk_your_actual_key_here \
  restaurant-recommender
```

Or with Docker Compose:
```yaml
environment:
  - LLM_PROVIDER=groq
  - GROQ_API_KEY=gsk_your_actual_key_here
```

---

## Validation

### Check Configuration

```python
import streamlit as st

# Display current configuration (for debugging)
st.write("Current Configuration:")
st.write(f"LLM Provider: {st.secrets.get('llm_provider', 'Not set')}")
st.write(f"Database Path: {st.secrets.get('database_path', 'Not set')}")
st.write(f"Server Port: {st.secrets.get('server', {}).get('port', 'Not set')}")
```

### Test API Connection

```python
import streamlit as st
from groq import Groq

try:
    client = Groq(api_key=st.secrets["groq_api_key"])
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": "Hello"}]
    )
    st.success("✅ Groq API connection successful!")
except Exception as e:
    st.error(f"❌ Groq API connection failed: {str(e)}")
```

---

## Summary

| Aspect | Details |
|--------|---------|
| **Local File** | `.streamlit/secrets.toml` |
| **Cloud Storage** | Streamlit Cloud app settings |
| **Format** | TOML |
| **Security** | Never commit to Git |
| **Access** | `st.secrets["key"]` |
| **Mapping** | Automatic to environment variables |

---

## Quick Reference

### Local Development
```bash
# 1. Edit .streamlit/secrets.toml
# 2. Add your API keys
# 3. Run: streamlit run streamlit_app.py
```

### Streamlit Cloud
```bash
# 1. Push to GitHub
# 2. Go to app settings → Secrets
# 3. Add secrets in TOML format
# 4. Save and redeploy
```

### Docker
```bash
# 1. Set environment variables
# 2. Run: docker run -e LLM_PROVIDER=groq -e GROQ_API_KEY=... app
```

---

**Happy configuring! 🚀**

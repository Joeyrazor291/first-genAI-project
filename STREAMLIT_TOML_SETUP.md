# Streamlit TOML Configuration Setup

## 📋 Overview

Your Streamlit application now supports TOML-based configuration for LLM API keys and other settings. This provides a secure, organized way to manage sensitive information.

---

## 🎯 What Was Created

### Configuration Files

1. **`.streamlit/secrets.toml`** (Main Configuration)
   - Your actual secrets file (local development)
   - Contains API keys and settings
   - **NEVER commit to GitHub**

2. **`.streamlit/secrets.toml.example`** (Template)
   - Example configuration with comments
   - Shows all available options
   - Safe to commit to GitHub

3. **`STREAMLIT_SECRETS_GUIDE.md`** (Detailed Guide)
   - Complete documentation
   - Setup instructions for all platforms
   - Troubleshooting guide

4. **`STREAMLIT_TOML_QUICK_REFERENCE.md`** (Quick Reference)
   - Copy-paste ready configurations
   - Quick setup instructions
   - Common configurations

### Updated Application

- **`streamlit_app.py`** (Updated)
  - Now reads from `.streamlit/secrets.toml`
  - Automatically maps secrets to environment variables
  - Supports both Groq and OpenRouter

---

## 🚀 Quick Start (Choose Your Platform)

### Local Development (Windows/Mac/Linux)

1. **Edit `.streamlit/secrets.toml`**:
   ```toml
   llm_provider = "groq"
   groq_api_key = "gsk_your_actual_key_here"
   database_path = "restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db"
   ```

2. **Run Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **App opens at**: http://localhost:8501

### Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add -A
   git commit -m "Add TOML configuration"
   git push origin main
   ```

2. **Go to Streamlit Cloud**:
   - https://share.streamlit.io
   - Click your app
   - Settings → Secrets

3. **Add TOML secrets**:
   ```toml
   llm_provider = "groq"
   groq_api_key = "gsk_your_actual_key_here"
   ```

4. **Save & redeploy**

### Docker

```bash
docker run -p 8501:8501 \
  -e LLM_PROVIDER=groq \
  -e GROQ_API_KEY=gsk_your_actual_key_here \
  restaurant-recommender
```

---

## 🔑 Getting Your API Key

### Groq (Free & Fast - Recommended)

```
1. Go to: https://console.groq.com
2. Sign up or log in
3. Navigate to: API Keys
4. Click: Create API Key
5. Copy the key (starts with "gsk_")
6. Add to secrets.toml:
   groq_api_key = "gsk_your_key_here"
```

### OpenRouter (Premium & Flexible)

```
1. Go to: https://openrouter.ai
2. Sign up or log in
3. Navigate to: Keys
4. Click: Create Key
5. Copy the key (starts with "sk-or-")
6. Add to secrets.toml:
   openrouter_api_key = "sk-or-your_key_here"
```

---

## 📝 TOML Configuration Examples

### Minimal Configuration (Just API Key)

```toml
llm_provider = "groq"
groq_api_key = "gsk_your_actual_key_here"
```

### Full Configuration (Recommended)

```toml
# LLM Provider
llm_provider = "groq"
groq_api_key = "gsk_your_actual_key_here"

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

# Client
[client]
showErrorDetails = true
toolbarMode = "viewer"

# Theme
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Production Configuration

```toml
llm_provider = "groq"
groq_api_key = "gsk_your_actual_key_here"
database_path = "/var/data/restaurant.db"

[server]
port = 8501
address = "0.0.0.0"
headless = true
runOnSave = false

[logger]
level = "warning"

[client]
showErrorDetails = false
toolbarMode = "minimal"
```

---

## 📂 File Structure

```
.streamlit/
├── config.toml                 # Streamlit configuration
├── secrets.toml                # Your actual secrets (local dev)
├── secrets.toml.example        # Template with examples
└── .gitignore                  # Ignore secrets.toml

TOML Configuration Files:
├── STREAMLIT_SECRETS_GUIDE.md           # Detailed guide
├── STREAMLIT_TOML_QUICK_REFERENCE.md    # Quick reference
└── STREAMLIT_TOML_SETUP.md              # This file
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Store API keys in `.streamlit/secrets.toml` (local)
- Use Streamlit Cloud secrets for production
- Never commit `secrets.toml` to GitHub
- Rotate API keys regularly
- Use environment-specific configurations
- Keep `.streamlit/secrets.toml` in `.gitignore`

### ❌ DON'T:
- Hardcode API keys in Python files
- Commit `secrets.toml` to version control
- Share API keys in chat or email
- Use the same key for dev and production
- Store secrets in plain text outside `.streamlit/`
- Push `secrets.toml` to GitHub

---

## 🛠️ Setup Checklist

### Local Development
- [ ] Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
- [ ] Add your Groq or OpenRouter API key
- [ ] Verify `.streamlit/secrets.toml` is in `.gitignore`
- [ ] Run `streamlit run streamlit_app.py`
- [ ] Test the app at http://localhost:8501

### Streamlit Cloud
- [ ] Push code to GitHub (without `secrets.toml`)
- [ ] Go to Streamlit Cloud app settings
- [ ] Add secrets in TOML format
- [ ] Save and redeploy
- [ ] Verify app works

### Docker
- [ ] Set environment variables
- [ ] Run Docker with `-e` flags
- [ ] Or use docker-compose with environment section
- [ ] Verify app works

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `.streamlit/secrets.toml` | Your actual secrets (local dev) |
| `.streamlit/secrets.toml.example` | Template with all options |
| `STREAMLIT_SECRETS_GUIDE.md` | Complete detailed guide |
| `STREAMLIT_TOML_QUICK_REFERENCE.md` | Quick reference & copy-paste configs |
| `STREAMLIT_TOML_SETUP.md` | This file - setup overview |

---

## 🔍 Verification

### Check Configuration

```python
import streamlit as st

# Display current configuration
st.write("LLM Provider:", st.secrets.get("llm_provider"))
st.write("Database Path:", st.secrets.get("database_path"))
st.write("Server Port:", st.secrets.get("server", {}).get("port"))
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

## 🐛 Troubleshooting

### Issue: "Secret not found" error

**Solution**:
1. Check `.streamlit/secrets.toml` exists
2. Verify key name is correct
3. Check TOML syntax is valid
4. Restart Streamlit

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

### Issue: Works locally but not on Streamlit Cloud

**Solution**:
1. Add secrets to Streamlit Cloud app settings
2. Use same key names as local `secrets.toml`
3. Redeploy app after adding secrets
4. Check app logs for errors

---

## 🎯 Next Steps

1. **Get API Key**:
   - Groq: https://console.groq.com
   - OpenRouter: https://openrouter.ai

2. **Configure Locally**:
   - Edit `.streamlit/secrets.toml`
   - Add your API key
   - Run `streamlit run streamlit_app.py`

3. **Test**:
   - Verify app loads
   - Test recommendations
   - Check AI explanations work

4. **Deploy**:
   - Choose platform (Streamlit Cloud, Docker, etc.)
   - Follow platform-specific setup
   - Add secrets to production environment

---

## 📚 Additional Resources

- **Streamlit Secrets Docs**: https://docs.streamlit.io/develop/concepts/connections/secrets-management
- **TOML Specification**: https://toml.io/
- **TOML Validator**: https://www.toml-lint.com/
- **Groq API Docs**: https://console.groq.com/docs
- **OpenRouter Docs**: https://openrouter.ai/docs

---

## 💡 Tips

- **Use Groq for development**: Free, fast, and easy to set up
- **Use OpenRouter for production**: More flexible, supports multiple models
- **Keep secrets.toml in .gitignore**: Never commit API keys
- **Rotate keys regularly**: For security
- **Use environment-specific configs**: Different keys for dev/prod
- **Test locally first**: Before deploying to production

---

## 🎉 Summary

Your Streamlit application now has:

✅ TOML-based configuration system
✅ Secure API key management
✅ Support for multiple LLM providers
✅ Environment-specific configurations
✅ Comprehensive documentation
✅ Quick setup guides
✅ Troubleshooting help

**You're ready to configure and deploy! 🚀**

---

## Quick Command Reference

```bash
# Local Development
streamlit run streamlit_app.py

# Docker
docker run -p 8501:8501 -e GROQ_API_KEY=your_key restaurant-recommender

# Docker Compose
docker-compose up -d

# Push to GitHub
git add -A
git commit -m "Add TOML configuration"
git push origin main
```

---

**Start with: `.streamlit/secrets.toml` and add your API key!**

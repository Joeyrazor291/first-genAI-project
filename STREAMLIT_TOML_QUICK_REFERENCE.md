# Streamlit TOML Configuration - Quick Reference

## 🚀 Quick Start

### Copy-Paste Ready TOML Configurations

#### Option 1: Groq (Free & Fast - Recommended)

```toml
llm_provider = "groq"
groq_api_key = "gsk_your_actual_key_here"
database_path = "restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db"

[server]
port = 8501
address = "0.0.0.0"
headless = true

[logger]
level = "info"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

#### Option 2: OpenRouter (Premium & Flexible)

```toml
llm_provider = "openrouter"
openrouter_api_key = "sk-or-your_actual_key_here"
database_path = "restaurant-recommendation/phase-1-data-pipeline/data/restaurant.db"

[server]
port = 8501
address = "0.0.0.0"
headless = true

[logger]
level = "info"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## 📋 File Locations

| Environment | Location | Action |
|-------------|----------|--------|
| **Local Dev** | `.streamlit/secrets.toml` | Create & edit file |
| **Streamlit Cloud** | App Settings → Secrets | Paste TOML content |
| **Docker** | Environment variables | Set via `-e` flag |

---

## 🔑 Getting API Keys

### Groq (Free)
1. Go to https://console.groq.com
2. Sign up/login
3. Click "API Keys"
4. Create new key
5. Copy key (starts with `gsk_`)

### OpenRouter (Paid)
1. Go to https://openrouter.ai
2. Sign up/login
3. Click "Keys"
4. Create new key
5. Copy key (starts with `sk-or-`)

---

## 📝 TOML Syntax Cheat Sheet

```toml
# String values
llm_provider = "groq"

# Numbers
port = 8501

# Booleans
headless = true

# Sections (tables)
[server]
port = 8501
address = "0.0.0.0"

# Nested sections
[theme]
primaryColor = "#FF6B35"
```

---

## 🛠️ Setup Instructions

### Local Development (3 Steps)

1. **Create file**:
   ```bash
   # File already exists at .streamlit/secrets.toml
   # Or copy from .streamlit/secrets.toml.example
   ```

2. **Add your API key**:
   ```toml
   llm_provider = "groq"
   groq_api_key = "gsk_your_actual_key_here"
   ```

3. **Run app**:
   ```bash
   streamlit run streamlit_app.py
   ```

### Streamlit Cloud (4 Steps)

1. **Push to GitHub**:
   ```bash
   git add -A
   git commit -m "Update Streamlit config"
   git push origin main
   ```

2. **Go to Streamlit Cloud**:
   - https://share.streamlit.io
   - Click your app
   - Settings → Secrets

3. **Paste TOML**:
   ```toml
   llm_provider = "groq"
   groq_api_key = "gsk_your_actual_key_here"
   ```

4. **Save & redeploy**

### Docker (1 Command)

```bash
docker run -p 8501:8501 \
  -e LLM_PROVIDER=groq \
  -e GROQ_API_KEY=gsk_your_actual_key_here \
  restaurant-recommender
```

---

## ✅ Verification

### Check Configuration Works

```python
import streamlit as st

# Display config
st.write("LLM Provider:", st.secrets.get("llm_provider"))
st.write("Database:", st.secrets.get("database_path"))
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
    st.success("✅ API working!")
except Exception as e:
    st.error(f"❌ Error: {e}")
```

---

## 🔒 Security Checklist

- [ ] API key is correct (copy-paste carefully)
- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] Never commit `secrets.toml` to GitHub
- [ ] Use different keys for dev/prod
- [ ] Rotate keys regularly
- [ ] Don't share keys in chat/email

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Secret not found" | Check file exists at `.streamlit/secrets.toml` |
| API key not working | Verify key is correct, not expired |
| TOML syntax error | Use https://www.toml-lint.com/ to validate |
| Works locally, not on Cloud | Add secrets to Streamlit Cloud app settings |
| Docker not reading secrets | Use `-e` flag or docker-compose environment |

---

## 📚 File References

| File | Purpose |
|------|---------|
| `.streamlit/secrets.toml` | Your actual secrets (local dev) |
| `.streamlit/secrets.toml.example` | Template with examples |
| `STREAMLIT_SECRETS_GUIDE.md` | Detailed guide |
| `STREAMLIT_TOML_QUICK_REFERENCE.md` | This file |

---

## 🎯 Common Configurations

### Minimal (Just API Key)
```toml
llm_provider = "groq"
groq_api_key = "gsk_your_key_here"
```

### Development
```toml
llm_provider = "groq"
groq_api_key = "gsk_your_key_here"

[logger]
level = "debug"

[client]
showErrorDetails = true
```

### Production
```toml
llm_provider = "groq"
groq_api_key = "gsk_your_key_here"

[logger]
level = "warning"

[client]
showErrorDetails = false
toolbarMode = "minimal"
```

---

## 🔗 Quick Links

- **Groq Console**: https://console.groq.com
- **OpenRouter**: https://openrouter.ai
- **Streamlit Cloud**: https://share.streamlit.io
- **TOML Validator**: https://www.toml-lint.com/
- **Streamlit Docs**: https://docs.streamlit.io

---

## 📖 Full Documentation

For detailed information, see:
- `STREAMLIT_SECRETS_GUIDE.md` - Complete guide
- `.streamlit/secrets.toml.example` - Full example with comments
- `STREAMLIT_SETUP.md` - Setup instructions

---

**Ready to configure? Start with the copy-paste TOML above! 🚀**

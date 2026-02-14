# Quick Start Guide

## Local Development

### 1. Setup
```bash
# Navigate to project directory
cd "C:\Users\hiran\Banking Application with database"

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### 2. Configure API Key
Edit `.streamlit/secrets.toml`:
```toml
MISTRAL_API_KEY = "your_api_key_here"
```

### 3. Run Locally
```bash
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

## Deploy to Streamlit Cloud

### Instructions:
1. Visit: https://streamlit.io/cloud
2. Sign in with GitHub account
3. Click "New app"
4. Configure:
   - Repository: `https://github.com/hirani60-ops/Banking-Bot`
   - Branch: `main`
   - Main file: `app.py`
5. Click "Deploy"
6. Once deployed, click app settings (⋮ menu)
7. Go to "Secrets" and add:
   ```
   MISTRAL_API_KEY = "nNKQYvoDfR3Z30ErVekiXoxClJQANBj2"
   ```
8. Your app will be live at a URL like:
   ```
   https://banking-bot-<username>.streamlit.app
   ```

## Project Structure
```
Banking-Bot/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
├── DEPLOYMENT.md                       # Deployment guide
├── QUICKSTART.md                       # This file
├── .env.example                        # Example environment variables
├── .gitignore                          # Git ignore rules
├── .streamlit/
│   ├── config.toml                    # Streamlit configuration
│   └── secrets.toml                   # Local secrets (not in git)
├── venv/                              # Virtual environment (not in git)
└── hbdb_banking_faqs (2) (1).csv      # FAQ database
```

## Features

✅ **AI-Powered**: Uses Mistral Large LLM  
✅ **Easy to Use**: Simple Streamlit interface  
✅ **FAQ Integration**: Loaded from CSV file  
✅ **Secure**: Environment variable-based API key management  
✅ **Interactive**: Real-time responses with spinner  
✅ **Professional**: Custom theming and configurations  

## Troubleshooting

**Q: "MISTRAL_API_KEY not found" error**
- A: Add the secret to Streamlit Cloud settings, not just `.env`

**Q: App is slow to respond**
- A: This is normal for first request. Streamlit Cloud may need to wake up cold instances

**Q: CSV file not found locally**
- A: Ensure filename matches exactly: `hbdb_banking_faqs (2) (1).csv`

**Q: Changes not reflecting on Streamlit Cloud**
- A: Push to `main` branch and wait for auto-deployment (1-2 minutes)

## Next Steps

1. Test locally: `streamlit run app.py`
2. Deploy to Streamlit Cloud (see instructions above)
3. Share the public URL with users
4. Monitor logs and update FAQs as needed

## Support

- Mistral AI Docs: https://docs.mistral.ai/
- Streamlit Docs: https://docs.streamlit.io/
- GitHub Repo: https://github.com/hirani60-ops/Banking-Bot

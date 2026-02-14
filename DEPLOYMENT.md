# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- Streamlit account (sign up at https://streamlit.io/cloud)

## Deployment Steps

### Step 1: Access Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Click "New app"

### Step 2: Configure Your App
1. **Repository**: Select `https://github.com/hirani60-ops/Banking-Bot`
2. **Branch**: Select `main`
3. **Main file path**: Enter `app.py`
4. Click "Deploy"

### Step 3: Add Secrets
1. Once deployed, go to your app's settings (... menu at top right)
2. Click "Secrets"
3. Add your Mistral API key:
   ```
   MISTRAL_API_KEY = "nNKQYvoDfR3Z30ErVekiXoxClJQANBj2"
   ```
4. Click "Save"

### Step 4: Access Your Bot
Your bot will be available at:
```
https://banking-bot.streamlit.app/
```

(The exact URL will depend on your Streamlit Cloud username and app name)

## Important Notes

⚠️ **Security**: 
- Never commit `.env` or `.streamlit/secrets.toml` to GitHub
- Use Streamlit Cloud's Secrets management for sensitive data
- Rotate your API key regularly

## Troubleshooting

### Issue: "MISTRAL_API_KEY not found"
- Ensure you've added the secret in Streamlit Cloud settings
- Wait a few moments for the secret to be applied
- Refresh the app

### Issue: "Module not found"
- Check that `requirements.txt` is in the root directory
- Ensure all dependencies are listed in `requirements.txt`
- Try redeploying the app

### Issue: CSV file not found
- Ensure `hbdb_banking_faqs (2) (1).csv` is in the repository root
- The filename must match exactly (case-sensitive on Linux servers)

## Monitoring Your Deployment

1. **View Logs**: Click the "ᐯ Manage app" dropdown → "View logs"
2. **Check App Status**: Monitor from the app list on Streamlit Cloud dashboard
3. **Update Code**: Push changes to GitHub's `main` branch - Streamlit will auto-redeploy

## Advanced Configuration

### Custom Domain (Streamlit Teams/Pro)
1. Go to app settings
2. Click "Custom domain"
3. Enter your domain name
4. Follow DNS configuration instructions

### Schedule Updates
If you update your FAQ CSV:
1. Commit changes to GitHub
2. Push to `main` branch
3. Streamlit Cloud will automatically redeploy

## Support

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Mistral AI Documentation**: https://docs.mistral.ai/
- **GitHub Issues**: https://github.com/hirani60-ops/Banking-Bot/issues

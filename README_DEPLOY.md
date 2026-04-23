# Deploying RadarCore to the Cloud

This guide explains how to deploy RadarCore to production using Streamlit Community Cloud (or similar platforms like Railway, Heroku, or Render) securely and with your environment protected.

## 1. Prerequisites

1. A **GitHub** account with the repository up to date.
2. A free account at [Streamlit Community Cloud](https://share.streamlit.io).
3. (Optional) A **Google Gemini** API Key for interactive AI reports (RAG).

## 2. Deployment Steps (Streamlit Cloud)

1. Go to `share.streamlit.io` and sign up by connecting your GitHub profile.
2. Click **"New app"**.
3. Select your repository (`radarcore`), the `main` branch, and set `app.py` as the "Main file path".
4. **Do NOT click 'Deploy' yet**. Click the button at the bottom labelled **"Advanced settings"** (or the gear icon under "Secrets").

## 3. Managing Secrets and Passwords

For the app to run in a protected mode *only for you*, you must configure the secrets in the cloud — the `.streamlit/secrets.toml` file is intentionally excluded from the repository via `.gitignore` and was not pushed.

Inside the **Secrets** section on the Streamlit deployment page (or via *Settings → Secrets* if you already deployed), paste the following:

```toml
[passwords]
# Change this password to your own!
admin = "CHANGE_THIS_PASSWORD"

# This forces the app to lock the interface until the correct password is entered.
IS_CLOUD_DEPLOYMENT = "true"
```

*Optionally, if you have a Google API key, add `GOOGLE_API_KEY = "your_key"` in the same block.*

**Cloud vs Local behaviour:**
The app contains an `is_cloud()` function embedded at the start of `app.py` that automatically detects the environment. On your local machine, no password will ever be required. On Streamlit Sharing, or when `IS_CLOUD_DEPLOYMENT = "true"`, the interface will be locked until the authorization secret is validated.

## 4. Post-Deployment UI Options

**RadarCore** has a sidebar toggle called **"Analysis Mode"**.
When running in the cloud with long scan jobs:

* **Automatic Mode**: Scans the full S&P 500, which can get throttled if Yahoo Finance blocks repeated requests (HTTP 429 Rate Limit error).
* **Watchlist Mode**: Scans exclusively against your private manual watchlist stored in SQLite. This is the safest and fastest configuration once on the cloud server. For full open-universe scanning, batch processing from a local machine is recommended.

# Trust Labs Analytics - GitHub Integration Guide

This document explains how to integrate this GitHub repository with Streamlit Cloud for easy deployment.

## Overview

```
GitHub Repository
    ↓
Streamlit Cloud
    ↓
Live Dashboard at https://trust-labs-analytics.streamlit.app
```

## Prerequisites

1. ✅ GitHub account (create at [github.com](https://github.com))
2. ✅ Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
3. ✅ This repository cloned/forked to your GitHub

---

## Step 1: Prepare Your GitHub Repository

### 1.1 Create/Update GitHub Repository

**Option A: Create New Repository**
```bash
# Navigate to your project folder
cd trust-labs-analytics

# Initialize Git
git init
git add .
git commit -m "Initial commit: Trust Labs Analytics Dashboard"

# Create repository on github.com first, then:
git remote add origin https://github.com/yourusername/trust-labs-analytics.git
git branch -M main
git push -u origin main
```

**Option B: Fork This Repository**
- Go to [GitHub](https://github.com)
- Find this repository
- Click "Fork" button
- Clone your fork:
```bash
git clone https://github.com/yourusername/trust-labs-analytics.git
```

### 1.2 Ensure Files Are in Place

Required files for Streamlit Cloud:
```
✅ app.py                    # Main application
✅ requirements.txt          # Python dependencies
✅ .streamlit/config.toml    # Streamlit configuration
✅ README.md                 # Documentation
✅ .gitignore                # What NOT to commit
✅ utils/                    # Helper modules (optional)
✅ data/.gitkeep             # Data folder placeholder
```

---

## Step 2: Connect to Streamlit Cloud

### 2.1 Sign Up / Log In

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub

### 2.2 Deploy New App

1. After logging in, click **"New app"** (top-right button)
2. Fill in the deployment form:

| Field | Value |
|-------|-------|
| **Repository** | `yourusername/trust-labs-analytics` |
| **Branch** | `main` |
| **Main file path** | `app.py` |

3. Click **"Deploy"** button

### 2.3 Wait for Deployment

- Streamlit will build and deploy your app
- This takes 2-5 minutes first time
- You'll see logs in the "Manage app" section
- App URL will be: `https://trust-labs-analytics.streamlit.app`

---

## Step 3: Add Secrets (Important!)

### 3.1 Store Database Credentials

1. In Streamlit Cloud dashboard, click your app
2. Click **"Manage app"** (top-right)
3. Go to **"Secrets"** tab
4. Add your secrets (one per line):

```toml
[database]
host = "localhost"
user = "admin"
password = "your_password"

[google_sheets]
api_key = "your_api_key"
spreadsheet_id = "your_sheet_id"
```

5. Click **"Save"**

### 3.2 Access Secrets in Your App

```python
import streamlit as st

# Access secrets safely
db_password = st.secrets["database"]["password"]
api_key = st.secrets["google_sheets"]["api_key"]
```

---

## Step 4: Data Management

### Option A: Use SQLite Database (Recommended)

1. **Create `trust_labs.db` locally**:
```bash
python utils/create_database.py
```

2. **Upload to repository** (NOT in .gitignore):
   - Move to repo root
   - Commit and push
```bash
git add trust_labs.db
git commit -m "Add database"
git push
```

### Option B: Use CSV Files in Data Folder

1. **Add data files to `data/` folder**:
```
data/
├── patients.csv
├── visits.csv
├── branches.csv
└── test_orders.csv
```

2. **Update `.gitignore`** to include/exclude data as needed:
```
# Exclude large CSV files
# data/

# Or include specific data:
!data/
data/.gitkeep
!data/sample_patients.csv
```

### Option C: Load from URL/API

Modify `app.py` to load from external source:
```python
import pandas as pd

# From URL
patients = pd.read_csv('https://yourdomain.com/data/patients.csv')

# From Google Sheets
@st.cache_data
def load_from_sheets():
    sheet_url = "..."
    return pd.read_csv(sheet_url)
```

---

## Step 5: Monitor & Maintain

### View Logs
1. Dashboard → Your App → "Manage app"
2. Click "Logs" tab
3. Check for errors

### Force Redeployment
```bash
# Make a change
git add .
git commit -m "Update app"
git push origin main

# Streamlit automatically redeploys when you push!
```

### Customize App URL (Optional)
In "Manage app" → Settings → "Custom URL":
- Change from `trust-labs-analytics.streamlit.app`
- To `mytrust-labs.streamlit.app` (requires Streamlit Community subscription)

---

## Workflow: Making Changes

Every time you update your code:

```bash
# 1. Make changes locally
# Edit app.py, requirements.txt, etc.

# 2. Test locally
streamlit run app.py

# 3. Commit and push
git add .
git commit -m "Describe your changes"
git push origin main

# 4. Streamlit Cloud automatically deploys!
# Watch at: https://share.streamlit.io (Manage app → Logs)
```

---

## Common Issues & Solutions

### "Module Not Found" Error
```
ModuleNotFoundError: No module named 'xyz'
```
**Solution**: Add missing package to `requirements.txt`
```bash
pip install xyz
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add xyz package"
git push
```

### Database Not Found
```
Error: unable to open database file
```
**Solution**: Commit database file or load from URL:
```bash
git add trust_labs.db
git commit -m "Add database"
git push
```

### Slow App Performance
**Solutions**:
- Enable caching (`@st.cache_data`)
- Optimize database queries
- Use `.gitattributes` for LFS (large files):
```
*.db filter=lfs diff=lfs merge=lfs -text
```

### Secrets Not Working
1. Verify format in `secrets.toml`:
```toml
[database]
password = "value"
```
2. Access correctly in code:
```python
pwd = st.secrets["database"]["password"]
```

---

## Advanced: CI/CD Automation

### Auto-test on Push

Create `.github/workflows/tests.yml`:
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

---

## Deployment Checklist

- [ ] GitHub repo created and pushed
- [ ] Streamlit account created
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets configured (passwords, API keys)
- [ ] Data files added (CSV or SQLite)
- [ ] `.gitignore` updated
- [ ] `requirements.txt` finalized
- [ ] README.md updated with your info
- [ ] Custom domain configured (optional)
- [ ] Monitoring setup (optional)

---

## Next Steps

1. **Share the link**: `https://trust-labs-analytics.streamlit.app`
2. **Monitor usage**: Dashboard → Analytics (Streamlit+)
3. **Add collaborators**: GitHub → Settings → Collaborators
4. **Scale up**: Upgrade to Streamlit+ for faster deployments

---

## Support

- 📖 [Streamlit Deployment Docs](https://docs.streamlit.io/deploy/streamlit-cloud)
- 💬 [Streamlit Community](https://discuss.streamlit.io)
- 🐛 [Report Issues](https://github.com/yourusername/trust-labs-analytics/issues)

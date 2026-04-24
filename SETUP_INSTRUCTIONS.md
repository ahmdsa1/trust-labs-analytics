# Setup Instructions

Complete guide to set up and deploy Trust Labs Analytics Dashboard.

## Local Development Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/trust-labs-analytics.git
cd trust-labs-analytics
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Prepare Your Data
1. **Create SQLite Database** or **Use CSV Files**:
   - Option A: Database (`trust_labs.db`) - Single source of truth
   - Option B: CSV files in `data/` folder - Simple file-based approach

2. **Required Data Files** in `data/` folder:
   ```
   data/
   ├── patients.csv          # Patient demographics & health info
   ├── visits.csv            # Visit records with timestamps
   ├── branches.csv          # Branch information & performance
   └── test_orders.csv       # Optional: Test ordering data
   ```

   See [DATA_SCHEMA.md](DATA_SCHEMA.md) for column requirements.

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`

---

## Database Setup (Optional but Recommended)

### Using SQLite Database

**Create from CSV files** (`trust_labs_pipeline/create_database.py`):
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('trust_labs.db')

# Load and create patients table
patients = pd.read_csv('data/patients.csv')
patients.to_sql('patients', conn, if_exists='replace', index=False)

# Load and create visits table
visits = pd.read_csv('data/visits.csv')
visits.to_sql('visits', conn, if_exists='replace', index=False)

# Load and create branches table
branches = pd.read_csv('data/branches.csv')
branches.to_sql('branches', conn, if_exists='replace', index=False)

conn.close()
print("✅ Database created: trust_labs.db")
```

**Or run the database creation script**:
```bash
python trust_labs_pipeline/create_database.py
```

---

## Configuration

### Streamlit Config (`.streamlit/config.toml`)
Customize the app appearance:
```toml
[theme]
primaryColor = "#667eea"      # Main color
backgroundColor = "#f8f9fa"   # Background
secondaryBackgroundColor = "#e8eef7"
textColor = "#202124"

[client]
showErrorDetails = true
toolbarMode = "developer"

[server]
port = 8501
headless = true
runOnSave = true
```

### Secrets (`.streamlit/secrets.toml`)
For database passwords or API keys:
```toml
[database]
host = "localhost"
user = "admin"
password = "your_password"

[google_sheets]
api_key = "your_api_key"
```

---

## Production Deployment

### Option 1: Streamlit Cloud (Easiest)

1. **Push code to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repo and `app.py`
   - Click "Deploy"

3. **Set Secrets**:
   - In Streamlit Cloud dashboard, click your app
   - Settings > Secrets
   - Paste your `.streamlit/secrets.toml` content
   - Save

### Option 2: Docker Container

1. **Create Dockerfile** (if not present):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

2. **Build and run**:
```bash
docker build -t trust-labs-analytics .
docker run -p 8501:8501 trust-labs-analytics
```

### Option 3: Heroku

1. **Create `Procfile`**:
```
web: sh setup.sh && streamlit run app.py
```

2. **Create `setup.sh`**:
```bash
mkdir -p ~/.streamlit/
echo "[server]" > ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
echo "port = $PORT" >> ~/.streamlit/config.toml
echo "enableCORS = false" >> ~/.streamlit/config.toml
```

3. **Deploy**:
```bash
heroku create your-app-name
git push heroku main
```

---

## Troubleshooting

### Database Connection Error
```
Error: unable to open database file
```
**Solution**: Ensure `trust_labs.db` exists in the root directory or use CSV files in `data/` folder.

### Module Import Error
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Activate virtual environment and reinstall requirements:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Data Not Loading
1. Check file paths in `config.py`
2. Verify CSV files exist in `data/` folder
3. Check file permissions
4. Run data validation: `python -m utils.data_loader`

### Port Already in Use
```
Address already in use: 0.0.0.0:8501
```
**Solution**: Use different port:
```bash
streamlit run app.py --server.port 8502
```

---

## Performance Optimization

- **Data Caching**: App caches data every 5 minutes (TTL=300s)
- **Database Indexes**: Create indexes on frequently queried columns:
  ```sql
  CREATE INDEX idx_patient_id ON visits(Patient_ID);
  CREATE INDEX idx_visit_date ON visits(Visit_Date);
  ```
- **Limit Data**: Filter by date range in queries for large datasets

---

## Security Checklist

- [ ] Never commit `.env` or `secrets.toml`
- [ ] Use `.gitignore` to exclude sensitive files
- [ ] Store credentials in Streamlit Cloud Secrets
- [ ] Validate all user inputs
- [ ] Use HTTPS in production
- [ ] Consider row-level security for multi-user deployments
- [ ] Encrypt sensitive data at rest

---

## Getting Help

- **Streamlit Docs**: https://docs.streamlit.io
- **GitHub Issues**: Create an issue in this repository
- **Streamlit Community**: https://discuss.streamlit.io
- **Contact**: your.email@example.com

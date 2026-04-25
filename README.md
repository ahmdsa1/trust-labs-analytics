# Trust Labs Healthcare Analytics Dashboard

A production-grade healthcare analytics dashboard built with **Streamlit**, featuring real-time patient churn prediction, loyalty analytics, branch benchmarking, and clinical insights.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

🔗 **Live Demo**: [https://fohosat.streamlit.app](https://fohosat.streamlit.app)

---

## 📊 Features

### Dashboard Pages
| Page | Description |
|------|-------------|
| 🏠 **Home** | Executive KPIs, alert banners, patient demographics |
| 🔍 **Patient Search** | Search patient profiles, visit history, risk scores |
| 👨‍⚕️ **Doctor Search** | Doctor profiles and performance lookup |
| 🏢 **Corporate Search** | Corporate contract management |
| 📊 **Analytics** | 7 tabs: Overview, Churn, Revenue, Forecasting, Clinical, Data Quality, Branch Benchmark |
| 📥 **Export** | Export any table to Excel/CSV |
| 📋 **Reports** | Generate full executive reports or custom reports |

### Key Analytics
- 🔐 **Authentication** — Role-based access (Admin/Viewer) with session management
- 🚨 **High-Risk Alerts** — Real-time alert banner for patients with churn risk ≥ 80
- 🔍 **Churn Prediction** — ML-based risk scoring with patient segmentation
- 📈 **Revenue Forecasting** — 3-month revenue predictions with confidence bands
- ⭐ **Loyalty Tiers** — Gold/Silver/Bronze classification with points
- 🏥 **Clinical Analytics** — Diabetes/hypertension prevalence tracking
- 🏢 **Branch Benchmarking** — Multi-location performance leaderboard
- 📊 **Data Quality Dashboard** — Missing data alerts and validation scores

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Local Installation

```bash
# 1. Clone
git clone https://github.com/ahmdsa1/trust-labs-analytics.git
cd trust-labs-analytics

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

### Default Login Credentials
| Username | Password | Role |
|----------|----------|------|
| `admin` | `trustlabs2024` | Full access |
| `viewer` | `view2024` | Read-only |

---

## 📁 Project Structure

```
trust-labs-analytics/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── trust_labs.db              # SQLite database (production data)
│
├── .streamlit/
│   ├── config.toml            # Streamlit theme & server config
│   └── secrets.toml.example   # Secrets template (copy to secrets.toml)
│
├── static/
│   └── styles.css             # Material Design 3 CSS
│
├── auth.py                    # Authentication module
├── alerts.py                  # High-risk patient alerts
├── reports.py                 # Report generation (Excel)
├── database.py                # Secure DB layer (parameterized queries)
├── components.py              # Reusable UI components
├── config.py                  # Centralized settings
├── logger.py                  # Structured logging
│
├── utils/                     # ETL Pipeline (CSV → SQLite)
│   ├── config.py
│   ├── data_loader.py
│   └── data_cleaner.py
│
└── .gitignore
```

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "v4.0: Enterprise features"
git push origin main
```

2. **Deploy**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub repo `ahmdsa1/trust-labs-analytics`
- Select `app.py` as the main file
- Click **Deploy**

3. **Configure Secrets** (optional)
- In Streamlit Cloud → Settings → Secrets
- Paste contents from `.streamlit/secrets.toml.example`
- Update passwords as needed

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t trust-labs .
docker run -p 8501:8501 trust-labs
```

---

## 🔐 Security

| Feature | Status |
|---------|--------|
| Password hashing (SHA-256) | ✅ |
| Session timeout (60 min) | ✅ |
| Role-based access control | ✅ |
| SQL injection prevention (parameterized queries) | ✅ |
| Input validation on all search fields | ✅ |
| Secrets managed via `secrets.toml` | ✅ |

---

## 📈 Performance

| Optimization | Implementation |
|-------------|----------------|
| Data caching | `@st.cache_data(ttl=3600)` |
| Resource caching | `@st.cache_resource` |
| Lazy loading | On-demand data fetching |
| Mobile responsive | CSS media queries |

---

## 🛠️ Development

### Adding New Features
1. Update `config.py` for new settings
2. Add module files (e.g., `analytics.py`)
3. Update `app.py` with new page/tab
4. Update `README.md` documentation

### Running Tests
```bash
python -m py_compile app.py
python -m py_compile auth.py alerts.py reports.py
```

---

## 📝 License

MIT License — see [LICENSE](LICENSE) file.

## 📧 Contact

- GitHub Issues: [github.com/ahmdsa1/trust-labs-analytics/issues](https://github.com/ahmdsa1/trust-labs-analytics/issues)
- Email: [ahmdsa1@proton.com](mailto:ahmdsa1@proton.com)
- WhatsApp: [+20 1143575727](https://wa.me/201143575727)

---

**Version**: 4.0.0 | **Last Updated**: July 2025

# Trust Labs Analytics Dashboard

A professional healthcare analytics dashboard built with **Streamlit** for the Trust Labs patient management system. Real-time insights into patient churn, loyalty, branch performance, and clinical analytics.

![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## 📊 Features

### Dashboard Pages
- **Executive Dashboard** - KPIs, demographics, trends, and branch performance
- **Patient Lookup** - Search and view individual patient profiles
- **Churn Analysis** - Identify high-risk patients and churn patterns
- **Loyalty & Points** - Patient tier management and rewards program
- **Branch Performance** - Multi-location analytics and benchmarking
- **Analytics & Trends** - Historical data analysis and forecasting
- **Export Reports** - Generate and download CSV/Excel reports

### Key Analytics
- 🔍 **Churn Prediction** - Risk scoring using machine learning
- 📊 **Patient Segmentation** - 5-cluster segmentation analysis
- 📈 **Revenue Forecasting** - 6-month revenue predictions
- ⭐ **Loyalty Tiers** - Gold/Silver/Bronze patient classification
- 🏥 **Clinical Analytics** - Diabetes/hypertension prevalence
- 🏢 **Branch Benchmarking** - Performance metrics across locations

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/trust-labs-analytics.git
cd trust-labs-analytics
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Prepare data**
Place your patient and visit CSV files in the `data/` folder:
```
data/
├── patients.csv
├── visits.csv
├── branches.csv
└── test_orders.csv
```

5. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
trust-labs-analytics/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── utils/
│   ├── config.py         # Configuration and settings
│   ├── data_loader.py    # Data loading utilities
│   ├── data_cleaner.py   # Data cleaning utilities
│   └── analytics.py      # Analytics calculations
├── pages/                # Multi-page app components
│   ├── dashboard.py
│   ├── patient_lookup.py
│   ├── churn_analysis.py
│   ├── loyalty.py
│   ├── branch_performance.py
│   ├── analytics.py
│   └── export.py
└── data/
    ├── patients.csv
    ├── visits.csv
    ├── branches.csv
    └── .gitkeep
```

## 🔧 Configuration

### Streamlit Config (`config.toml`)
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#e8eef7"
textColor = "#202124"
font = "sans serif"
```

### Data Requirements
- **patients.csv**: Patient demographics, health conditions, retention data
- **visits.csv**: Visit records, dates, branches, timing
- **branches.csv**: Branch locations, performance metrics
- **test_orders.csv**: Test ordering and pricing data

## 📊 Data Schema

### Patients
- Patient_ID, Age_Group, Gender, Patient_Type
- Has_Diabetes, Has_Hypertension, Distance_Category
- Total_Visits_Expected, Retention_Category
- Churn_Risk_Score, Patient_Tier

### Visits
- Visit_Date, Visit_Number, Visit_Day, Visit_Month
- Patient_ID, Branch_ID, Branch_Name, Branch_City
- Visit_Hour, Visit_Time, Is_Fasting_Time
- Is_Weekend, Is_Peak_Hour, Is_Return_Visit

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and connect your GitHub repository
4. Select this repository and `app.py` as the main file

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Heroku
```bash
git push heroku main
heroku logs --tail
```

## 🔐 Security & Data Privacy

- Patient data should be in a secure SQLite database (included in `.gitignore`)
- Credentials and API keys go in `.streamlit/secrets.toml` (not in version control)
- Consider row-level security for multi-tenant deployments
- HIPAA compliance considerations for healthcare data

## 📈 Performance Optimization

- Caching implemented with `@st.cache_data` and `@st.cache_resource`
- Data updates refresh every 5 minutes (TTL: 300s)
- Database connections are pooled
- Plotly charts are optimized for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Support & Contact

For issues, questions, or suggestions:
- Open an [issue on GitHub](https://github.com/yourusername/trust-labs-analytics/issues)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Analytics powered by Plotly, Pandas, Scikit-learn
- Data sourced from Trust Labs patient database

---

**Last Updated**: April 2026 | **Version**: 1.0.0

"""
Trust Labs Healthcare Analytics Dashboard
Material Design 3 + Google Analytics 4 Aesthetic
FIXED VERSION - All Issues Resolved
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ── Phase 4: Enterprise imports ──
import config
from auth import (
    init_auth_state, require_auth, render_login_form,
    render_logout_button, is_admin, AUTH_ENABLED
)
from alerts import render_alert_banner, render_alert_table, get_alert_summary
from reports import build_report_excel, build_custom_report, format_report_filename, build_report_pdf

st.set_page_config(
    page_title="Trust Labs Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# AUTHENTICATION GATE
# ============================================================

init_auth_state()

if AUTH_ENABLED and not st.session_state.get("authenticated", False):
    render_login_form()
    st.stop()

# User is authenticated — show logout in sidebar later


# ============================================================
# FULL MATERIAL DESIGN 3 CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;600;700&family=Google+Sans+Display:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');

/* ── FORCE LIGHT THEME ───────────────────────────────────── */
html, body, [class*="css"], .stApp {
  background: #f8f9fa !important;
  color: #202124 !important;
}
.main .block-container {
  padding: 1.5rem 2rem !important;
  max-width: 1600px !important;
}
.stMarkdown, .stMarkdown *, .stText,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
[data-testid="stText"], .element-container,
p, span, li, h1, h2, h3, h4, h5, h6 {
  color: #202124 !important;
}

/* ── SIDEBAR COLLAPSE BUTTON — ALWAYS VISIBLE ────────────── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebarCollapsedControl"],
button[data-testid="baseButton-headerNoPadding"] {
  visibility: visible !important;
  display: flex !important;
  opacity: 1 !important;
}

/* ── SIDEBAR ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid #dadce0 !important;
}
[data-testid="stSidebar"] * { color: #202124 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio label {
  display: flex !important; align-items: center !important;
  gap: 10px !important; padding: 10px 14px !important;
  border-radius: 8px !important; color: #5f6368 !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  cursor: pointer !important; transition: background .2s, color .2s !important;
  font-family: 'Google Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: #e8f0fe !important; color: #1a73e8 !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
  display: none !important;
}

/* ── TABS ────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: #ffffff !important; border-radius: 16px 16px 0 0 !important;
  padding: 0 16px !important; border-bottom: 1px solid #dadce0 !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  height: 52px !important;
  font-family: 'Google Sans', sans-serif !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  color: #5f6368 !important; border-bottom: 3px solid transparent !important;
  padding: 0 20px !important; background: transparent !important;
}
.stTabs [aria-selected="true"] {
  color: #1a73e8 !important; border-bottom-color: #1a73e8 !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: #ffffff !important; border-radius: 0 0 16px 16px !important;
  padding: 20px !important; border: 1px solid #dadce0 !important;
  border-top: none !important;
}

/* ── INPUTS ───────────────────────────────────────────────── */
.stTextInput label, .stSelectbox label, .stMultiSelect label,
.stNumberInput label, .stRadio label, .stCheckbox label {
  color: #5f6368 !important; font-size: 0.8125rem !important;
  font-weight: 500 !important; font-family: 'Google Sans', sans-serif !important;
}
.stTextInput input, .stTextInput > div > div > input {
  color: #202124 !important; background: #ffffff !important;
  border: 1px solid #dadce0 !important; border-radius: 8px !important;
}
.stSelectbox *, .stMultiSelect * { color: #202124 !important; }
.stSelectbox > div > div, .stMultiSelect > div > div {
  background: #ffffff !important;
}
[data-baseweb="select"] > div,
[data-baseweb="popover"] > div,
[role="listbox"], [role="option"] {
  background: #ffffff !important; color: #202124 !important;
}
[role="option"]:hover { background: #e8f0fe !important; }
[data-baseweb="tag"] { background: #e8f0fe !important; color: #1a73e8 !important; }
.stNumberInput input {
  color: #202124 !important; background: #ffffff !important;
  border: 1px solid #dadce0 !important;
}

/* ── BUTTONS ─────────────────────────────────────────────── */
.stButton > button {
  font-family: 'Google Sans', sans-serif !important; font-weight: 500 !important;
  font-size: 0.875rem !important; background: #1a73e8 !important;
  color: #ffffff !important; border: none !important;
  border-radius: 8px !important; padding: 0.625rem 1.5rem !important;
  box-shadow: 0 1px 3px rgba(60,64,67,.15) !important;
  transition: box-shadow .2s, transform .15s !important;
}
.stButton > button:hover {
  box-shadow: 0 4px 12px rgba(60,64,67,.15) !important;
  transform: translateY(-1px) !important;
}
.stDownloadButton > button {
  background: #ffffff !important; color: #1a73e8 !important;
  border: 1px solid #dadce0 !important; border-radius: 8px !important;
  font-weight: 500 !important; font-family: 'Google Sans', sans-serif !important;
}
.stDownloadButton > button:hover { background: #e8f0fe !important; }

/* ── DATAFRAME ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: 12px !important; border: 1px solid #dadce0 !important;
  overflow: hidden !important;
}

/* ── HIDE STREAMLIT CHROME ───────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stMetric"] { display: none !important; }

/* ── CUSTOM COMPONENTS ───────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-header h1 {
  font-family: 'Google Sans Display', sans-serif !important;
  font-size: 1.75rem !important; font-weight: 500 !important;
  color: #202124 !important; margin: 0 0 4px 0 !important;
}
.page-header p { font-size: 0.875rem; color: #5f6368; margin: 0; }

.kpi-grid { display: grid; gap: 12px; margin-bottom: 1.25rem; }
.kpi-card {
  background: #ffffff; border-radius: 16px; padding: 20px 22px;
  box-shadow: 0 1px 3px rgba(60,64,67,.15),0 1px 2px rgba(60,64,67,.12);
  border: 1px solid #dadce0; position: relative; overflow: hidden;
  transition: box-shadow .2s;
}
.kpi-card:hover { box-shadow: 0 4px 12px rgba(60,64,67,.15); }
.kpi-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--acc, #1a73e8); border-radius: 16px 16px 0 0;
}
.kpi-label {
  font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--acc, #1a73e8);
  font-family: 'Google Sans', sans-serif; margin-bottom: 6px;
}
.kpi-value {
  font-size: 1.9rem; font-weight: 500; color: #202124;
  font-family: 'Google Sans Display', sans-serif; line-height: 1.1; margin-bottom: 8px;
}
.kpi-trend {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.72rem; font-weight: 500; padding: 3px 10px;
  border-radius: 100px; font-family: 'Google Sans', sans-serif;
}
.kpi-trend.up     { background: #e6f4ea; color: #137333; }
.kpi-trend.down   { background: #fce8e6; color: #c5221f; }
.kpi-trend.neutral{ background: #fef7e0; color: #b06000; }
.kpi-icon { position: absolute; top: 16px; right: 18px; font-size: 1.75rem; opacity: 0.1; }

/* ── CHART SECTION CARD ─────────────────────────────────── */
.section-title {
  font-family: 'Google Sans', sans-serif !important; font-size: 0.9375rem !important;
  font-weight: 600 !important; color: #202124 !important;
  margin: 0 0 14px 0 !important; display: flex; align-items: center; gap: 8px;
  padding: 18px 20px 0 20px;
  background: #ffffff;
  border-radius: 16px 16px 0 0;
  border: 1px solid #dadce0;
  border-bottom: none;
}
.section-subtitle {
  font-size: 0.8rem; color: #5f6368; margin: -10px 0 14px 0;
  padding: 0 20px 12px 20px;
  background: #ffffff;
  border-left: 1px solid #dadce0;
  border-right: 1px solid #dadce0;
}
.chart-body {
  background: #ffffff;
  border-radius: 0 0 16px 16px;
  border: 1px solid #dadce0;
  border-top: none;
  padding: 0 16px 16px 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(60,64,67,.15);
}

/* Stand-alone cards (no chart inside — just text/table) */
.info-card {
  background: #ffffff; border-radius: 16px; padding: 20px 22px;
  box-shadow: 0 1px 3px rgba(60,64,67,.15); border: 1px solid #dadce0;
  margin-bottom: 12px;
}
.info-card-title {
  font-family: 'Google Sans', sans-serif; font-size: 0.9375rem;
  font-weight: 600; color: #202124; margin: 0 0 14px 0;
}

.infl-banner {
  background: linear-gradient(90deg,#fef7e0 0%,#e8f0fe 100%);
  border-left: 4px solid #fbbc04; padding: 14px 18px;
  border-radius: 8px; margin-bottom: 16px; font-size: 0.86rem; color: #3c4043;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PLOTLY GOOGLE THEME
# ============================================================

def google_theme(fig, height=350):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showline=True, linecolor="#dadce0",
                   tickfont=dict(size=11, color="#5f6368", family="Roboto"),
                   title_font=dict(size=11, color="#5f6368", family="Google Sans")),
        yaxis=dict(showgrid=True, gridcolor="#f1f3f4", showline=False,
                   tickfont=dict(size=11, color="#5f6368", family="Roboto"),
                   title_font=dict(size=11, color="#5f6368", family="Google Sans")),
        font=dict(family="Roboto, sans-serif", size=11, color="#202124"),
        margin=dict(t=20, b=30, l=40, r=20),
        height=height,
        hoverlabel=dict(bgcolor="#ffffff", font_size=11,
                       font_family="Roboto", bordercolor="#dadce0"),
        legend=dict(font=dict(size=11, color="#5f6368"),
                   bgcolor="rgba(0,0,0,0)", orientation="h",
                   yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def google_donut(vals, names, colors, hole=0.6):
    fig = px.pie(values=vals, names=names, color=names,
                 color_discrete_map=dict(zip(names, colors)))
    fig.update_traces(hole=hole, textposition="outside",
                      textinfo="percent+label",
                      textfont=dict(size=11, color="#202124"),
                      marker=dict(line=dict(color="#ffffff", width=3)))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
                      margin=dict(t=10, b=10, l=10, r=10),
                      font=dict(family="Google Sans, sans-serif", size=11, color="#202124"))
    return fig

def safe_vline(fig, x_datetime):
    xs = x_datetime.strftime("%Y-%m-%d")
    fig.add_shape(type="line", x0=xs, x1=xs, y0=0, y1=1,
                  xref="x", yref="paper",
                  line=dict(color="#9aa0a6", width=1.5, dash="solid"))
    fig.add_annotation(x=xs, y=0.97, xref="x", yref="paper",
                       text="Forecast →", showarrow=False, xanchor="left",
                       font=dict(size=10, color="#5f6368"),
                       bgcolor="rgba(255,255,255,0.85)", borderpad=3)

# ============================================================
# CHART SECTION CARD HELPERS
# ============================================================

def sec_title(title, subtitle=""):
    html = f'<div class="section-title">{title}</div>'
    if subtitle:
        html += f'<div class="section-subtitle">{subtitle}</div>'
    st.markdown(html, unsafe_allow_html=True)

def chart_start():
    st.markdown('<div class="chart-body">', unsafe_allow_html=True)

def chart_end():
    st.markdown('</div>', unsafe_allow_html=True)

def info_card_start(title):
    st.markdown(f'<div class="info-card"><div class="info-card-title">{title}</div>', unsafe_allow_html=True)

def info_card_end():
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# KPI CARD HELPERS
# ============================================================

def kpi_card(label, value, trend_text, trend_dir="neutral", icon="", accent="#1a73e8"):
    cls   = {"up":"up","down":"down","neutral":"neutral"}.get(trend_dir, "neutral")
    arrow = {"up":"↑","down":"↓","neutral":"→"}.get(trend_dir, "→")
    return f"""
<div class="kpi-card" style="--acc:{accent}">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <span class="kpi-trend {cls}">{arrow}&nbsp;{trend_text}</span>
</div>"""

def kpi_row(cards, cols=5):
    return (f'<div class="kpi-grid" style="grid-template-columns:repeat({cols},1fr)">'
            + "".join(cards) + "</div>")

# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():
    return sqlite3.connect("trust_labs.db", check_same_thread=False)

conn = get_connection()

# ============================================================
# DATA LOADERS
# ============================================================

@st.cache_data(ttl=3600)
def load_patients():
    df = pd.read_sql("SELECT * FROM patients", conn)
    df = df.rename(columns={
        "patient_id": "Patient_ID",
        "age_group": "Age_Group",
        "gender": "Gender",
        "has_diabetes": "Has_Diabetes",
        "has_hypertension": "Has_Hypertension",
        "patient_tier": "patient_tier",
        "churn_risk_score": "churn_risk_score",
        "loyalty_points": "loyalty_points",
        "churn_risk_category": "churn_risk_category",
    })
    return df

@st.cache_data(ttl=3600)
def load_visits():
    df = pd.read_sql("SELECT * FROM visits", conn)
    df = df.rename(columns={
        "visit_id": "Visit_ID",
        "patient_id": "Patient_ID",
        "branch_name_en": "Branch_Name",
        "visit_date": "Visit_Date",
        "visit_month_dt": "Visit_Month",
        "visit_day": "Visit_Day",
        "visit_hour": "Visit_Hour",
        "is_weekend": "Is_Weekend",
        "is_peak_hour": "Is_Peak_Hour",
        "is_return_visit": "Is_Return_Visit",
        "amount_paid": "Amount_Paid",
        "patient_tier": "patient_tier",
        "loyalty_points": "loyalty_points",
        "churn_risk_category": "churn_risk_category",
    })
    df["Visit_Date"]  = pd.to_datetime(df["Visit_Date"],  errors="coerce")
    df["Visit_Month"] = pd.to_datetime(df["Visit_Month"], errors="coerce")
    return df

@st.cache_data(ttl=3600)
def load_doctors():
    try:
        df = pd.read_sql("SELECT * FROM doctors", conn)
        df = df.rename(columns={"specialty_en": "specialty"})
        return df
    except Exception:
        return pd.DataFrame({"doctor_id": [], "actual_referrals": []})

@st.cache_data(ttl=3600)
def load_corporates():
    try:
        df = pd.read_sql("SELECT * FROM corporates", conn)
        df = df.rename(columns={"company_name_en": "company_name"})
        return df
    except Exception:
        return pd.DataFrame({"corporate_id": [], "actual_visits": []})

@st.cache_data(ttl=3600)
def load_branches():
    df = pd.read_sql("SELECT * FROM branches", conn)
    df = df.rename(columns={
        "branch_name_en": "Branch_Name",
        "city_en": "Branch_City",
    })
    return df

@st.cache_data(ttl=3600)
def load_monthly_trends():
    try:
        df = pd.read_sql("SELECT * FROM monthly_trends", conn)
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_monthly_revenue():
    try:
        df = pd.read_sql("SELECT * FROM monthly_revenue", conn)
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_revenue_by_test():
    return pd.read_sql(
        "SELECT * FROM revenue_by_test ORDER BY total_revenue DESC LIMIT 20", conn)

# ============================================================
# SEARCH HELPERS
# ============================================================

def search_patient_by_id(pid):
    q = "SELECT * FROM patients WHERE LOWER(Patient_ID)=LOWER(?)"
    r = pd.read_sql(q, conn, params=(pid,))
    return r if not r.empty else None

def search_doctor_by_id(did):
    try:
        q = "SELECT * FROM doctors WHERE LOWER(Doctor_ID)=LOWER(?)"
        r = pd.read_sql(q, conn, params=(did,))
        return r if not r.empty else None
    except Exception:
        return None

def search_corporate_by_id(cid):
    try:
        q = "SELECT * FROM corporates WHERE LOWER(Corporate_ID)=LOWER(?)"
        r = pd.read_sql(q, conn, params=(cid,))
        return r if not r.empty else None
    except Exception:
        return None

def get_patient_visits(pid):
    q = """SELECT Visit_Date, Branch_Name, Visit_Time, Visit_Day
            FROM visits WHERE LOWER(Patient_ID)=LOWER(?)
            ORDER BY Visit_Date DESC"""
    df = pd.read_sql(q, conn, params=(pid,))
    df["Visit_Date"] = pd.to_datetime(df["Visit_Date"], errors="coerce")
    return df

# ============================================================
# EXPORT HELPERS
# ============================================================

def export_to_excel(df):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    return out.getvalue()

def export_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# ============================================================
# ANALYTICS HELPERS
# ============================================================

def predict_visits(monthly_trends_df, months_ahead=3):
    if monthly_trends_df.empty:
        return pd.DataFrame(), 0
    df = monthly_trends_df.copy().sort_values("visit_month").reset_index(drop=True)
    df["month_num"] = range(len(df))
    X = df[["month_num"]].values
    y = df["total_visits"].values
    model = LinearRegression()
    model.fit(X, y)
    residuals = y - model.predict(X)
    std_err = np.std(residuals)
    last_num = df["month_num"].max()
    future_nums = np.array([[last_num + i] for i in range(1, months_ahead + 1)])
    preds = model.predict(future_nums).astype(int)
    last_date = df["visit_month"].max()
    future_dates = [last_date + timedelta(days=30*i) for i in range(1, months_ahead + 1)]
    return pd.DataFrame({
        "visit_month": future_dates,
        "predicted_visits": preds,
        "lower": (preds - std_err).astype(int),
        "upper": (preds + std_err).astype(int),
    }), std_err

def compute_cagr(initial, final, months):
    if initial <= 0 or final <= 0 or months <= 0:
        return 0.0
    try:
        years = months / 12.0
        return ((final / initial) ** (1.0 / years) - 1.0) * 100.0
    except Exception:
        return 0.0

def build_real_revenue_from_visits(visits_df, annual_inflation=0.33):
    avg_revenue_per_visit = 150
    monthly = visits_df.groupby("Visit_Month").agg({"Visit_Date": "count"}).reset_index()
    monthly.columns = ["visit_month", "total_visits"]
    monthly = monthly.sort_values("visit_month").reset_index(drop=True)
    monthly["total_revenue"] = monthly["total_visits"] * avg_revenue_per_visit
    monthly["total_profit"]  = monthly["total_revenue"] * 0.65
    if monthly.empty or len(monthly) < 2:
        return pd.DataFrame()
    n = len(monthly)
    deflators = [(1 + annual_inflation) ** (i / 12.0) for i in range(n)]
    monthly["deflator"]      = deflators
    monthly["real_revenue"]  = monthly["total_revenue"] / monthly["deflator"]
    monthly["real_profit"]   = monthly["total_profit"]  / monthly["deflator"]
    monthly["inflation_tax"] = monthly["total_revenue"] - monthly["real_revenue"]
    rv0 = monthly["real_revenue"].iloc[0]
    nv0 = monthly["total_revenue"].iloc[0]
    monthly["real_index"]    = monthly["real_revenue"]  / rv0 * 100
    monthly["nominal_index"] = monthly["total_revenue"] / nv0 * 100
    monthly["month_label"]   = monthly["visit_month"].dt.strftime("%b %Y")
    return monthly


def compute_monthly_metrics(visits_df):
    """Compute monthly visit and patient metrics from visits data for trend analysis."""
    if visits_df.empty or "Visit_Month" not in visits_df.columns:
        return pd.DataFrame()
    monthly = visits_df.groupby("Visit_Month").agg({
        "Patient_ID": "nunique",
        "Visit_Date": "count"
    }).reset_index()
    monthly.columns = ["visit_month", "unique_patients", "total_visits"]
    monthly = monthly.sort_values("visit_month").reset_index(drop=True)
    monthly["avg_visits_per_patient"] = monthly["total_visits"] / monthly["unique_patients"].clip(lower=1)
    return monthly


def get_trend_indicator(monthly_df, metric_col, mode="pct"):
    """
    Compute trend indicator from monthly data.
    mode: 'pct' for percentage change, 'abs' for absolute change.
    Returns: (trend_string, direction)
    """
    if monthly_df is None or monthly_df.empty or len(monthly_df) < 2 or metric_col not in monthly_df.columns:
        return "—", "neutral"
    latest = monthly_df[metric_col].iloc[-1]
    prev = monthly_df[metric_col].iloc[-2]
    if pd.isna(latest) or pd.isna(prev) or prev == 0:
        return "—", "neutral"
    if mode == "pct":
        change = (latest / prev - 1) * 100
        if abs(change) < 0.05:
            return "—", "neutral"
        direction = "up" if change > 0 else "down"
        return f"{change:+.1f}%", direction
    elif mode == "abs":
        change = latest - prev
        if abs(change) < 0.01:
            return "—", "neutral"
        direction = "up" if change > 0 else "down"
        return f"{change:+.1f}", direction
    return "—", "neutral"


def perform_patient_segmentation(patients_df, n_clusters=5):
    """
    Perform KMeans clustering on patients for segmentation analysis.
    Returns: (patients_df_with_clusters, cluster_summary, cluster_names)
    """
    feature_cols = ["total_visits", "loyalty_points", "churn_risk_score", 
                    "days_since_last_visit"]
    available_cols = [c for c in feature_cols if c in patients_df.columns]
    
    if len(available_cols) < 3:
        return patients_df, pd.DataFrame(), {}
    
    df = patients_df.copy()
    for col in available_cols:
        df[col] = df[col].fillna(df[col].median())
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[available_cols])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)
    
    summary = df.groupby("cluster")[available_cols].mean().round(1)
    summary["count"] = df.groupby("cluster").size()
    summary = summary.reset_index()
    
    names = {}
    for _, row in summary.iterrows():
        cid = int(row["cluster"])
        visits = row.get("total_visits", 0)
        risk = row.get("churn_risk_score", 50)
        loyalty = row.get("loyalty_points", 0)
        
        if visits > summary["total_visits"].median() and risk < summary["churn_risk_score"].median():
            names[cid] = "Champions"
        elif visits > summary["total_visits"].median() and risk >= summary["churn_risk_score"].median():
            names[cid] = "At-Risk Loyal"
        elif visits <= summary["total_visits"].median() and risk < summary["churn_risk_score"].median():
            names[cid] = "New Potentials"
        elif loyalty > summary["loyalty_points"].median():
            names[cid] = "Dormant VIPs"
        else:
            names[cid] = "Need Attention"
    
    return df, summary, names


def compute_data_quality(df, table_name="Table"):
    """Compute data quality metrics for a DataFrame."""
    if df.empty:
        return {
            "table": table_name,
            "total_rows": 0,
            "total_cols": 0,
            "missing_pct": 0,
            "duplicate_rows": 0,
            "completeness_score": 0
        }
    
    total_cells = df.size
    missing_cells = df.isna().sum().sum()
    missing_pct = (missing_cells / total_cells) * 100 if total_cells > 0 else 0
    duplicate_rows = df.duplicated().sum()
    completeness = 100 - missing_pct
    
    return {
        "table": table_name,
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "missing_pct": round(missing_pct, 1),
        "duplicate_rows": duplicate_rows,
        "completeness_score": round(completeness, 1)
    }

def build_real_revenue(mr_df, annual_inflation=0.33):
    if mr_df.empty or len(mr_df) < 2:
        return pd.DataFrame()
    df = (mr_df.sort_values("visit_month").dropna(subset=["total_revenue"])
          .copy().reset_index(drop=True))
    if df.empty or len(df) < 2:
        return df
    n = len(df)
    deflators           = [(1 + annual_inflation) ** (i / 12.0) for i in range(n)]
    df["deflator"]      = deflators
    df["real_revenue"]  = df["total_revenue"] / df["deflator"]
    if "total_profit" in df.columns:
        df["real_profit"] = df["total_profit"] / df["deflator"]
    df["inflation_tax"] = df["total_revenue"] - df["real_revenue"]
    rv0 = df["real_revenue"].iloc[0]
    nv0 = df["total_revenue"].iloc[0]
    df["real_index"]    = df["real_revenue"]  / rv0 * 100
    df["nominal_index"] = df["total_revenue"] / nv0 * 100
    df["month_label"]   = df["visit_month"].dt.strftime("%b %Y")
    return df

# ============================================================
# LOAD EVERYTHING
# ============================================================

patients_data   = load_patients()
visits_data     = load_visits()
doctors_data    = load_doctors()
corporates_data = load_corporates()
branches_data   = load_branches()
monthly_trends  = load_monthly_trends()
monthly_revenue = load_monthly_revenue()
high_risk_count = int((patients_data["churn_risk_category"] == "High Risk").sum()) if len(patients_data) > 0 else 0
active_docs     = int((doctors_data["actual_referrals"] > 0).sum()) if len(doctors_data) > 0 else 0
active_corps    = int((corporates_data["actual_visits"] > 0).sum()) if len(corporates_data) > 0 else 0

# Compute monthly metrics once for global use (Home + Analytics pages)
monthly_metrics = compute_monthly_metrics(visits_data)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
<div style="padding:12px 6px 20px 6px">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="font-size:1.6rem"></span>
    <div>
      <div style="font-family:'Google Sans Display',sans-serif;font-size:1rem;
                  font-weight:700;color:#202124;line-height:1.2">Trust Labs</div>
      <div style="font-size:.7rem;color:#5f6368">Healthcare Analytics</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="margin:0 0 12px;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)

    page = st.radio("nav",
        ["  Home","  Patient Search","‍️  Doctor Search",
         "  Corporate Search","‍️  Doctors","  Analytics","  Export"," Reports"],
        label_visibility="collapsed")

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)
    st.markdown("""<div style="font-size:.7rem;font-weight:600;text-transform:uppercase;
letter-spacing:.8px;color:#5f6368;margin-bottom:10px;font-family:'Google Sans',sans-serif"
>Quick Stats</div>""", unsafe_allow_html=True)

    st.markdown(kpi_row([
        kpi_card("Patients",f"{len(patients_data):,}","","neutral","","#1a73e8"),
        kpi_card("Visits",f"{len(visits_data):,}","","neutral","","#34a853")
    ],2), unsafe_allow_html=True)
    st.markdown(kpi_row([
        kpi_card("Doctors",f"{active_docs}","","neutral","‍️","#fbbc04"),
        kpi_card("At Risk",f"{high_risk_count}","","down","️","#ea4335")
    ],2), unsafe_allow_html=True)

    # ── Feature 1: Global Date Range Filter ──
    st.markdown("---")
    st.markdown("**Date Range**")
    min_date = visits_data["Visit_Date"].min().date() if not visits_data.empty and pd.notna(visits_data["Visit_Date"].min()) else datetime(2024,1,1).date()
    max_date = visits_data["Visit_Date"].max().date() if not visits_data.empty and pd.notna(visits_data["Visit_Date"].max()) else datetime.today().date()
    date_range = st.date_input(
        "Filter all pages",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="global_date_range"
    )
    if len(date_range) == 2:
        st.session_state["date_start"] = pd.Timestamp(date_range[0])
        st.session_state["date_end"] = pd.Timestamp(date_range[1])

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)
    
    # Phase 4: Logout button
    render_logout_button()
    
    # ── Feature 2: Data Freshness Indicator ──
    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)
    last_load = st.session_state.get("last_load_time", datetime.now())
    minutes_ago = int((datetime.now() - last_load).total_seconds() / 60)
    color = "#34a853" if minutes_ago < 30 else "#fbbc04" if minutes_ago < 60 else "#ea4335"
    st.markdown(f"""
<div style="font-size:0.7rem;color:{color};text-align:center;padding:4px 0">
  ● Data refreshed {minutes_ago}m ago
</div>""", unsafe_allow_html=True)
    if st.button("↺ Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.session_state["last_load_time"] = datetime.now()
        st.rerun()

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;font-size:0.7rem;color:#9aa0a6">
Updated {datetime.now().strftime("%b %d, %Y • %H:%M")}</div>""",
                unsafe_allow_html=True)

# ============================================================
# PAGE: HOME
# ============================================================

if page == "  Home":
    st.markdown("""<div class="page-header">
<h1>Analytics Dashboard</h1>
<p>Professional healthcare intelligence platform</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    avg_visits  = len(visits_data) / len(patients_data) if len(patients_data) > 0 else 0
    avg_loyalty = patients_data["loyalty_points"].mean() if len(patients_data) > 0 else 0
    high_risk_pct = high_risk_count / len(patients_data) * 100 if len(patients_data) > 0 else 0

    # Real trends from pre-computed monthly_metrics
    patients_trend, patients_dir = get_trend_indicator(monthly_metrics, "unique_patients", "pct")
    visits_trend, visits_dir = get_trend_indicator(monthly_metrics, "total_visits", "pct")
    avg_trend, avg_dir = get_trend_indicator(monthly_metrics, "avg_visits_per_patient", "abs")
    risk_trend, risk_dir = "—", "neutral"
    loyalty_trend, loyalty_dir = "—", "neutral"

    # Phase 4: High-risk patient alerts
    render_alert_banner(patients_data)
    
    st.markdown(kpi_row([
        kpi_card("Total Patients", f"{len(patients_data):,}", patients_trend, patients_dir, "", "#1a73e8"),
        kpi_card("Total Visits", f"{len(visits_data):,}", visits_trend, visits_dir, "", "#34a853"),
        kpi_card("Avg Visits/Patient", f"{avg_visits:.1f}", avg_trend, avg_dir, "", "#fbbc04"),
        kpi_card("High Risk %", f"{high_risk_pct:.1f}%", risk_trend, risk_dir, "️", "#ea4335"),
        kpi_card("Avg Loyalty", f"{avg_loyalty:.0f}", loyalty_trend, loyalty_dir, "", "#9334e6")
    ], 5), unsafe_allow_html=True)
    
    # Phase 4: Alert details expander
    render_alert_table(patients_data)

    c1, c2 = st.columns(2)
    with c1:
        sec_title(" Gender Distribution")
        chart_start()
        if "Gender" in patients_data.columns:
            gender_counts = patients_data["Gender"].value_counts()
            fig = google_donut(gender_counts.values, gender_counts.index, ["#1a73e8", "#ea4335"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Gender data not available")
        chart_end()

    with c2:
        sec_title("️ Churn Risk Levels")
        chart_start()
        if "churn_risk_category" in patients_data.columns:
            risk_counts = patients_data["churn_risk_category"].value_counts()
            fig = google_donut(risk_counts.values, risk_counts.index,
                              ["#34a853", "#fbbc04", "#ea4335"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Risk data not available")
        chart_end()

    sec_title(" Monthly Visit Trends")
    chart_start()
    if len(monthly_metrics) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_metrics["visit_month"], y=monthly_metrics["total_visits"],
            mode="lines+markers", name="Total Visits",
            line=dict(color="#1a73e8", width=3), marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=monthly_metrics["visit_month"], y=monthly_metrics["unique_patients"],
            mode="lines+markers", name="Unique Patients",
            line=dict(color="#34a853", width=2, dash="dash"), marker=dict(size=8)
        ))
        google_theme(fig, height=320)
        fig.update_layout(
            xaxis=dict(tickformat="%b %Y", dtick="M1"),
            yaxis_title="Count",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No monthly trend data available")
    chart_end()

    st.markdown(kpi_row([
        kpi_card("Gold Tier", f"{len(patients_data[patients_data['patient_tier']=='Gold']) if 'patient_tier' in patients_data.columns else 0:,}",
                f"{len(patients_data[patients_data['patient_tier']=='Gold'])/len(patients_data)*100:.1f}%" if len(patients_data) > 0 and 'patient_tier' in patients_data.columns else "0%",
                "neutral", "", "#fbbc04"),
        kpi_card("Active Doctors", f"{active_docs}/{len(doctors_data)}", "active", "up", "‍️", "#34a853"),
        kpi_card("Active Contracts", f"{active_corps}/{len(corporates_data)}", "active", "up", "", "#1a73e8"),
        kpi_card("Top Branch", branches_data.nlargest(1, "total_visits")["Branch_Name"].values[0] if len(branches_data) > 0 else "N/A",
                "Leading", "neutral", "", "#9334e6")
    ], 4), unsafe_allow_html=True)

# ============================================================
# PAGE: PATIENT SEARCH
# ============================================================

elif page == "  Patient Search":
    st.markdown("""<div class="page-header">
<h1>Patient Search</h1>
<p>Search and analyze patient records</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    tab1, tab2 = st.tabs(["🆔 ID Lookup", " Advanced Search"])

    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            patient_id = st.text_input("Patient ID", placeholder="e.g., P0000000001")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button(" Search", type="primary", use_container_width=True)

        if search_btn and patient_id:
            patient = search_patient_by_id(patient_id)
            if patient is None:
                st.error(f" Patient ID '{patient_id}' not found!")
            else:
                st.success(f" Patient Found: **{patient_id.upper()}**")

                tier    = patient["patient_tier"].values[0] if "patient_tier" in patient.columns else "Unknown"
                loyalty = int(patient["loyalty_points"].values[0]) if "loyalty_points" in patient.columns else 0
                risk    = int(patient["churn_risk_score"].values[0]) if "churn_risk_score" in patient.columns else 0
                visits  = int(patient["total_visits"].values[0]) if "total_visits" in patient.columns else 0
                days    = int(patient["days_since_last_visit"].values[0]) if "days_since_last_visit" in patient.columns else 0

                st.markdown(kpi_row([
                    kpi_card("Tier", tier, "", "neutral", "", "#1a73e8"),
                    kpi_card("Loyalty", str(loyalty), "points", "up", "⭐", "#fbbc04"),
                    kpi_card("Risk Score", str(risk),
                            "Low" if risk<30 else "Medium" if risk<60 else "High",
                            "neutral" if risk<30 else "down", "️",
                            "#ea4335" if risk>=60 else "#fbbc04"),
                    kpi_card("Visits", str(visits), "", "neutral", "", "#34a853"),
                    kpi_card("Days Since", str(days), "last visit", "neutral", "", "#9334e6")
                ], 5), unsafe_allow_html=True)

                info_card_start("Patient Information")
                st.dataframe(patient.T, use_container_width=True)
                info_card_end()

                patient_visits = get_patient_visits(patient_id)
                if not patient_visits.empty:
                    info_card_start(f"Visit History ({len(patient_visits)} visits)")
                    st.dataframe(patient_visits, hide_index=True,
                                use_container_width=True, height=300)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button(" Download Excel",
                                         export_to_excel(patient_visits),
                                         f"patient_{patient_id}_visits.xlsx",
                                         use_container_width=True)
                    with c2:
                        st.download_button(" Download CSV",
                                         export_to_csv(patient_visits),
                                         f"patient_{patient_id}_visits.csv",
                                         use_container_width=True)
                    info_card_end()

    with tab2:
        info_card_start(" Advanced Filters")
        c1, c2, c3 = st.columns(3)
        with c1:
            tier_filter   = st.multiselect("Tier", ["Gold", "Silver", "Bronze"]) if "patient_tier" in patients_data.columns else []
            risk_filter   = st.multiselect("Risk", ["Low Risk", "Medium Risk", "High Risk"]) if "churn_risk_category" in patients_data.columns else []
        with c2:
            age_filter    = st.multiselect("Age Group", sorted(patients_data["Age_Group"].unique())) if "Age_Group" in patients_data.columns else []
            gender_filter = st.selectbox("Gender", ["All", "Male", "Female"]) if "Gender" in patients_data.columns else "All"
        with c3:
            min_visits  = st.number_input("Min Visits", 0, step=1)
            min_loyalty = st.number_input("Min Loyalty", 0, step=10)

        if st.button(" Apply Filters", type="primary"):
            results = patients_data.copy()
            if tier_filter and "patient_tier" in results.columns:   
                results = results[results["patient_tier"].isin(tier_filter)]
            if risk_filter and "churn_risk_category" in results.columns:   
                results = results[results["churn_risk_category"].isin(risk_filter)]
            if age_filter and "Age_Group" in results.columns:    
                results = results[results["Age_Group"].isin(age_filter)]
            if gender_filter != "All" and "Gender" in results.columns: 
                results = results[results["Gender"] == gender_filter]
            if min_visits > 0 and "total_visits" in results.columns:  
                results = results[results["total_visits"] >= min_visits]
            if min_loyalty > 0 and "loyalty_points" in results.columns: 
                results = results[results["loyalty_points"] >= min_loyalty]

            st.markdown(f'<p style="color:#5f6368;font-size:.85rem">Found {len(results):,} patients</p>',
                       unsafe_allow_html=True)
            display_cols = ["Patient_ID", "Age_Group", "Gender", "patient_tier",
                           "loyalty_points", "churn_risk_category", "total_visits"]
            display_cols = [c for c in display_cols if c in results.columns]
            st.dataframe(results[display_cols],
                        hide_index=True, use_container_width=True, height=400)
            st.download_button(" Export Results", export_to_excel(results), "search_results.xlsx")
        info_card_end()

# ============================================================
# PAGE: DOCTOR SEARCH
# ============================================================

elif page == "‍️  Doctor Search":
    st.markdown("""<div class="page-header">
<h1>Doctor Performance</h1>
<p>Track and analyze doctor referral metrics</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    c1, c2 = st.columns([3, 1])
    with c1:
        doctor_id = st.text_input("Doctor ID", placeholder="e.g., DOC00096")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button(" Search", type="primary", use_container_width=True)

    if search_btn and doctor_id:
        doctor = search_doctor_by_id(doctor_id)
        if doctor is None or doctor.empty:
            st.error(f" Doctor ID '{doctor_id}' not found!")
        else:
            doc_name = doctor["doctor_name"].values[0] if "doctor_name" in doctor.columns else doctor_id
            st.success(f" Doctor Found: **{doc_name}**")
            refs    = int(doctor["actual_referrals"].values[0]) if "actual_referrals" in doctor.columns else 0
            patients_ref = int(doctor["unique_patients_referred"].values[0]) if "unique_patients_referred" in doctor.columns else 0
            revenue = float(doctor["total_revenue_generated"].values[0]) if "total_revenue_generated" in doctor.columns else 0
            perf    = doctor["performance_category"].values[0] if "performance_category" in doctor.columns else "N/A"
            specialty = doctor["specialty"].values[0] if "specialty" in doctor.columns else "Unknown"
            st.markdown(kpi_row([
                kpi_card("Specialty", specialty, "", "neutral", "", "#1a73e8"),
                kpi_card("Referrals", f"{refs:,}", "", "up", "", "#34a853"),
                kpi_card("Patients", f"{patients_ref:,}", "unique", "up", "", "#fbbc04"),
                kpi_card("Revenue", f"{revenue/1000:.1f}K EGP", "generated", "up", "", "#9334e6"),
                kpi_card("Performance", perf, "",
                        "up" if perf=="Exceeds Expectations" else "neutral",
                        "⭐", "#34a853" if perf=="Exceeds Expectations" else "#fbbc04")
            ], 5), unsafe_allow_html=True)
            info_card_start("Complete Doctor Profile")
            st.dataframe(doctor.T, use_container_width=True)
            info_card_end()

    info_card_start("All Doctors Performance")
    display_doctors = doctors_data
    if len(doctors_data) > 0:
        display_cols = ["doctor_id", "doctor_name", "specialty", "actual_referrals",
            "unique_patients_referred", "total_revenue_generated", "performance_category"]
        display_cols = [c for c in display_cols if c in display_doctors.columns]
        display_doctors = display_doctors[display_cols]
        if "actual_referrals" in display_doctors.columns:
            display_doctors = display_doctors.sort_values("actual_referrals", ascending=False)
        st.dataframe(display_doctors, hide_index=True, use_container_width=True, height=400)
        st.download_button(" Export Doctors", export_to_excel(display_doctors), "doctors_performance.xlsx")
    else:
        st.info("No doctor data available")
    info_card_end()

# ============================================================
# PAGE: CORPORATE SEARCH
# ============================================================

elif page == "  Corporate Search":
    st.markdown("""<div class="page-header">
<h1>Corporate Contracts</h1>
<p>Manage and analyze corporate partnerships</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    tab_search, tab_gap = st.tabs([" Contract Search", " Utilization Gap"])

    with tab_search:
        c1, c2 = st.columns([3, 1])
        with c1:
            corp_id = st.text_input("Corporate ID", placeholder="e.g., CORP023")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button(" Search", type="primary", use_container_width=True)

        corp = None
        if search_btn and corp_id:
            corp = search_corporate_by_id(corp_id)
        if corp is None or corp.empty:
            st.error(f" Corporate ID '{corp_id}' not found!")
        else:
            st.success(f" Contract Found: **{corp['company_name'].values[0]}**")
            emp     = int(corp["employee_count"].values[0]) if "employee_count" in corp.columns else 0
            active  = int(corp["unique_employees"].values[0]) if "unique_employees" in corp.columns else 0
            util    = float(corp["actual_utilization_rate"].values[0]) * 100 if "actual_utilization_rate" in corp.columns else 0
            revenue = float(corp["total_revenue"].values[0]) if "total_revenue" in corp.columns else 0
            health  = corp["contract_health"].values[0] if "contract_health" in corp.columns else "N/A"
            st.markdown(kpi_row([
                kpi_card("Employees", f"{emp:,}", "total", "neutral", "", "#1a73e8"),
                kpi_card("Active", f"{active:,}", f"{active/emp*100:.0f}%" if emp > 0 else "0%", "up", "", "#34a853"),
                kpi_card("Utilization", f"{util:.1f}%", "rate",
                        "up" if util > 50 else "neutral", "", "#fbbc04"),
                kpi_card("Revenue", f"{revenue/1000:.1f}K EGP", "total", "up", "", "#9334e6"),
                kpi_card("Health", health, "",
                        "up" if health=="Excellent" else "neutral" if health=="Good" else "down",
                        "️", "#34a853" if health=="Excellent" else "#fbbc04")
            ], 5), unsafe_allow_html=True)
            info_card_start("Contract Details")
            st.dataframe(corp.T, use_container_width=True)
            info_card_end()

    with tab_search:
        info_card_start("All Corporate Contracts")
        display_corps = corporates_data
        if len(corporates_data) > 0:
            display_cols = ["corporate_id", "company_name", "industry", "employee_count",
                "unique_employees", "total_revenue", "contract_health"]
            display_cols = [c for c in display_cols if c in display_corps.columns]
            display_corps = display_corps[display_cols].sort_values("total_revenue", ascending=False)
            st.dataframe(display_corps, hide_index=True, use_container_width=True, height=400)
            st.download_button(" Export Contracts", export_to_excel(display_corps), "corporate_contracts.xlsx")
        else:
            st.info("No corporate data available")
        info_card_end()

    with tab_gap:
        if not corporates_data.empty and "employee_count" in corporates_data.columns:
            gap_df = corporates_data.copy()
            gap_df["utilization_pct"] = (gap_df["unique_employees"] / gap_df["employee_count"] * 100).round(1)
            gap_df["inactive_employees"] = gap_df["employee_count"] - gap_df["unique_employees"]
            avg_revenue_per_employee = (gap_df["total_revenue"] / gap_df["unique_employees"].clip(lower=1)).mean()
            gap_df["gap_egp"] = (gap_df["inactive_employees"] * avg_revenue_per_employee).round(0)
            gap_df["health"] = gap_df["utilization_pct"].apply(
                lambda x: "🟢 Excellent" if x >= 20 else ("🟡 Good" if x >= 10 else ("🟠 At-Risk" if x >= 5 else " Critical"))
            )

            total_gap = gap_df["gap_egp"].sum()
            critical_count = len(gap_df[gap_df["utilization_pct"] < 5])

            st.markdown(kpi_row([
                kpi_card("Total Revenue Gap", f"{total_gap/1e6:.2f}M EGP", "untapped", "down", "", "#ea4335"),
                kpi_card("Critical Contracts", str(critical_count), "< 5% utilization", "down", "", "#ea4335"),
                kpi_card("Avg Utilization", f"{gap_df['utilization_pct'].mean():.1f}%", "across contracts", "neutral", "", "#fbbc04"),
                kpi_card("Total Inactive", f"{gap_df['inactive_employees'].sum():,}", "employees", "neutral", "", "#9334e6"),
            ], 4), unsafe_allow_html=True)

            sec_title(" Revenue Gap by Contract", "Sorted by untapped EGP opportunity")
            chart_start()
            top_gap = gap_df.nlargest(15, "gap_egp")
            fig = px.bar(top_gap, x="gap_egp", y="company_name", orientation="h",
                         color="utilization_pct", color_continuous_scale="RdYlGn",
                         text=top_gap["gap_egp"].apply(lambda x: f"{x/1000:.0f}K EGP"))
            fig.update_traces(textposition="outside")
            google_theme(fig, height=400)
            fig.update_layout(xaxis_title="Gap (EGP)", yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            info_card_start("All Contracts — Utilization Overview")
            display_cols = ["company_name", "employee_count", "unique_employees", "utilization_pct", "gap_egp", "health"]
            display_cols = [c for c in display_cols if c in gap_df.columns]
            st.dataframe(gap_df[display_cols].sort_values("gap_egp", ascending=False),
                         hide_index=True, use_container_width=True)
            st.download_button(" Export Gap Analysis", export_to_excel(gap_df[display_cols]), "utilization_gap.xlsx")
            info_card_end()
        else:
            st.info("Employee count data required for utilization gap analysis")



# ============================================================
# PAGE: DOCTOR RANKING DASHBOARD
# ============================================================

elif page == "‍️  Doctors":
    st.markdown("""<div class="page-header">
<h1>Doctor Ranking Dashboard</h1>
<p>Performance, risk alerts, and branch flow analysis</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    from alerts import get_at_risk_doctors

    tab_rank, tab_risk, tab_flow = st.tabs([" Ranking", "️ At-Risk Alerts", " Branch Flow"])

    # ── TAB 1: RANKING ──
    with tab_rank:
        if not doctors_data.empty and "actual_referrals" in doctors_data.columns:
            docs_ranked = get_at_risk_doctors(doctors_data.copy())
            docs_ranked = docs_ranked.sort_values("actual_referrals", ascending=False)

            total_docs = len(docs_ranked)
            active_count = len(docs_ranked[docs_ranked["status"] == "Active"])
            atrisk_count = len(docs_ranked[docs_ranked["status"] == "At-Risk"])
            dormant_count = len(docs_ranked[docs_ranked["status"] == "Dormant"])

            st.markdown(kpi_row([
                kpi_card("Total Doctors", str(total_docs), "", "neutral", "‍️", "#1a73e8"),
                kpi_card("Active", str(active_count), f"{active_count/total_docs*100:.0f}%" if total_docs > 0 else "0%", "up", "", "#34a853"),
                kpi_card("At-Risk", str(atrisk_count), f"{atrisk_count/total_docs*100:.0f}%" if total_docs > 0 else "0%", "down", "️", "#fbbc04"),
                kpi_card("Dormant", str(dormant_count), f"{dormant_count/total_docs*100:.0f}%" if total_docs > 0 else "0%", "down", "", "#ea4335"),
            ], 4), unsafe_allow_html=True)

            sec_title(" Top 15 Doctors by Referrals")
            chart_start()
            top15 = docs_ranked.head(15)
            fig = px.bar(top15, x="actual_referrals", y="doctor_name", orientation="h",
                         color="actual_referrals", color_continuous_scale="Blues",
                         text="actual_referrals")
            fig.update_traces(textposition="outside")
            google_theme(fig, height=400)
            fig.update_layout(xaxis_title="Referrals", yaxis_title=None, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            if "specialty" in docs_ranked.columns:
                sec_title(" Referrals by Specialty")
                chart_start()
                spec = docs_ranked.groupby("specialty")["actual_referrals"].sum().reset_index()
                fig = px.pie(spec, values="actual_referrals", names="specialty", hole=0.6)
                fig.update_traces(textposition="outside", textinfo="percent+label",
                                  marker=dict(line=dict(color="#ffffff", width=3)))
                fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                                  plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
                                  margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                chart_end()

            info_card_start("All Doctors — Sortable Performance Table")
            display_cols = ["doctor_name", "specialty", "actual_referrals",
                            "unique_patients_referred", "total_revenue_generated", "status"]
            display_cols = [c for c in display_cols if c in docs_ranked.columns]
            def color_status(val):
                if val == "Active": return "background-color:#e6f4ea;color:#137333"
                if val == "At-Risk": return "background-color:#fef3e8;color:#b06000"
                if val == "Dormant": return "background-color:#fce8e6;color:#c5221f"
                return ""
            try:
                styled = docs_ranked[display_cols].style.map(color_status, subset=["status"])
            except AttributeError:
                styled = docs_ranked[display_cols].style.applymap(color_status, subset=["status"])
            st.dataframe(styled, hide_index=True, use_container_width=True, height=400)
            info_card_end()
        else:
            st.info("No doctor data available")

    # ── TAB 2: AT-RISK ALERTS ──
    with tab_risk:
        if not doctors_data.empty and "actual_referrals" in doctors_data.columns:
            docs_risk = get_at_risk_doctors(doctors_data.copy())
            at_risk_df = docs_risk[docs_risk["status"].isin(["At-Risk", "Dormant"])]
            if not at_risk_df.empty:
                revenue_at_risk = at_risk_df["total_revenue_generated"].sum() if "total_revenue_generated" in at_risk_df.columns else 0
                st.markdown(kpi_row([
                    kpi_card("At-Risk Doctors", str(len(at_risk_df)), "", "down", "️", "#ea4335"),
                    kpi_card("Revenue at Risk", f"{revenue_at_risk/1000:.1f}K EGP", "potential loss", "down", "", "#ea4335"),
                ], 2), unsafe_allow_html=True)

                def color_risk_row(val):
                    if val == "Dormant": return "background-color:#fce8e6;color:#c5221f;font-weight:600"
                    if val == "At-Risk": return "background-color:#fef3e8;color:#b06000;font-weight:600"
                    return ""
                display_cols = ["doctor_name", "specialty", "actual_referrals",
                                "unique_patients_referred", "total_revenue_generated", "status"]
                display_cols = [c for c in display_cols if c in at_risk_df.columns]
                try:
                    styled = at_risk_df[display_cols].style.map(color_risk_row, subset=["status"])
                except AttributeError:
                    styled = at_risk_df[display_cols].style.applymap(color_risk_row, subset=["status"])
                st.dataframe(styled, hide_index=True, use_container_width=True, height=400)
                st.download_button(" Export At-Risk List", export_to_excel(at_risk_df[display_cols]),
                                   "at_risk_doctors.xlsx", use_container_width=True)
            else:
                st.success(" No at-risk doctors detected!")
        else:
            st.info("No doctor data available")

    # ── TAB 3: BRANCH FLOW ──
    with tab_flow:
        # Load doctor_branch table for branch flow analysis
        sec_title("🩺 Doctor Referral Flow", "Which doctors drive branch volume?")
        try:
            doctor_branch = pd.read_sql("SELECT * FROM doctor_branch LIMIT 1", conn)
            if not doctor_branch.empty:
                doctor_branch = pd.read_sql("SELECT * FROM doctor_branch", conn)
                if not doctor_branch.empty and not doctors_data.empty:
                    # Merge with doctors to get specialties
                    flow = doctor_branch.merge(
                        doctors_data[["doctor_id", "specialty"]],
                        on="doctor_id",
                        how="left"
                    )
                    if "branch_name_ar" in flow.columns and "specialty" in flow.columns and "referrals" in flow.columns:
                        chart_start()
                        fig = px.bar(flow, x="referrals", y="branch_name_ar", orientation="h",
                                     color="specialty", barmode="stack")
                        google_theme(fig, height=400)
                        fig.update_layout(xaxis_title="Referrals", yaxis_title="Branch")
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        chart_end()

                        info_card_start("Branch Flow Summary")
                        summary = flow.groupby(["branch_name_ar", "specialty"])["referrals"].sum().reset_index()
                        st.dataframe(summary, hide_index=True, use_container_width=True)
                        info_card_end()
                    else:
                        st.warning("Required columns missing for branch flow visualization")
                else:
                    st.info("Branch flow data not available")
            else:
                st.error("doctor_branch table not found. Rebuilding database...")
        except Exception as e:
            st.error(f"Error loading branch flow data: {str(e)}. Please refresh data using the sidebar button.")

# ============================================================
# PAGE: ANALYTICS
# ============================================================

elif page == "  Analytics":
    st.markdown("""<div class="page-header">
<h1>Analytics Dashboard</h1>
<p>Patients • Revenue • Inflation-adjusted CAGR • 3-month forecast</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
        [" Overview", "️ Churn", " Revenue & Inflation (CAGR)", " Predictive Trends", " Clinical Insights", " Data Quality", " Branch Ops", " Revenue Mix", "️ Branch Compare"])

    # ── TAB 1: OVERVIEW ──
    with tab1:
        n = len(patients_data)
        if "patient_tier" in patients_data.columns:
            gold   = len(patients_data[patients_data["patient_tier"]=="Gold"])
            silver = len(patients_data[patients_data["patient_tier"]=="Silver"])
            bronze = len(patients_data[patients_data["patient_tier"]=="Bronze"])
        else:
            gold = silver = bronze = 0

        st.markdown(kpi_row([
            kpi_card(" Gold",   f"{gold:,}",   f"{gold/n*100:.1f}%" if n > 0 else "0%",   "neutral","","#fbbc04"),
            kpi_card(" Silver", f"{silver:,}", f"{silver/n*100:.1f}%" if n > 0 else "0%", "neutral","","#9aa0a6"),
            kpi_card(" Bronze", f"{bronze:,}", f"{bronze/n*100:.1f}%" if n > 0 else "0%", "neutral","","#cd7f32"),
            kpi_card("Avg Loyalty", f"{patients_data['loyalty_points'].mean() if 'loyalty_points' in patients_data.columns else 0:.0f}", "points","up","⭐","#1a73e8")
        ], 4), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec_title(" Patient Tiers")
            chart_start()
            if "patient_tier" in patients_data.columns:
                tier_counts = patients_data["patient_tier"].value_counts()
                fig = google_donut(tier_counts.values, tier_counts.index,
                                  ["#fbbc04", "#9aa0a6", "#cd7f32"])
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Tier data not available")
            chart_end()

        with c2:
            sec_title(" Top 5 Branches")
            chart_start()
            if len(branches_data) > 0:
                top5 = branches_data.nlargest(5, "total_visits")
                fig = px.bar(top5, x="total_visits", y="Branch_Name", orientation="h",
                            color="performance_score", color_continuous_scale="Blues")
                google_theme(fig, height=280)
                fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Total Visits")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Branch data not available")
            chart_end()

        sec_title(" Age Distribution")
        chart_start()
        if "Age_Group" in patients_data.columns:
            age_dist = patients_data["Age_Group"].value_counts().sort_index()
            fig = px.bar(x=age_dist.index, y=age_dist.values,
                        color=age_dist.values, color_continuous_scale="Viridis")
            google_theme(fig, height=300)
            fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Age group data not available")
        chart_end()

        # ── Feature 5: Day-of-Week × Hour Heatmap ──
        sec_title(" Visit Heatmap — Day × Hour", "When are patients most likely to visit?")
        chart_start()
        if "Visit_Day" in filtered_visits.columns and "Visit_Hour" in filtered_visits.columns:
            day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            heat_df = filtered_visits.groupby(["Visit_Day", "Visit_Hour"]).size().reset_index(name="visits")
            heat_pivot = heat_df.pivot(index="Visit_Day", columns="Visit_Hour", values="visits").fillna(0)
            heat_pivot = heat_pivot.reindex([d for d in day_order if d in heat_pivot.index])
            # Convert numpy types to native Python types for JSON serialization
            heat_pivot.columns = [int(c) for c in heat_pivot.columns]
            heat_pivot = heat_pivot.astype(int)
            fig = px.imshow(heat_pivot, color_continuous_scale="Blues", aspect="auto",
                            labels=dict(x="Hour of Day", y="Day of Week", color="Visits"))
            fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              margin=dict(t=10, b=30, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Visit_Day and Visit_Hour columns required for heatmap")
        chart_end()

        # ── MoM Growth Analysis ──
        sec_title(" Month-over-Month Growth",
                  "Track visit and patient growth rates month-over-month")
        chart_start()
        if len(monthly_metrics) > 1:
            mom = monthly_metrics.copy()
            mom["visit_growth"] = mom["total_visits"].pct_change() * 100
            mom["patient_growth"] = mom["unique_patients"].pct_change() * 100
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=mom["visit_month"].iloc[1:], y=mom["visit_growth"].iloc[1:],
                name="Visit Growth %", marker_color="#1a73e8"
            ))
            fig.add_trace(go.Bar(
                x=mom["visit_month"].iloc[1:], y=mom["patient_growth"].iloc[1:],
                name="Patient Growth %", marker_color="#34a853"
            ))
            google_theme(fig, height=300)
            fig.update_layout(
                barmode="group",
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="Growth %",
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Need at least 2 months of data for MoM analysis")
        chart_end()

        # ── Feature 7: No-Show Cost Estimator ──
        info_card_start(" No-Show Cost Estimator")
        avg_revenue = visits_data["Amount_Paid"].mean() if "Amount_Paid" in visits_data.columns else 150
        no_show_rate = st.slider("Estimated No-Show Rate (%)", 0, 30, 8, key="noshowslider")
        total_bookings = len(filtered_visits)
        estimated_noshows = int(total_bookings * no_show_rate / 100)
        cost = estimated_noshows * avg_revenue
        st.markdown(kpi_row([
            kpi_card("Est. No-Shows", f"{estimated_noshows:,}", f"{no_show_rate}% rate", "down", "", "#ea4335"),
            kpi_card("Revenue Lost", f"{cost/1000:.1f}K EGP", "per period", "down", "", "#ea4335"),
            kpi_card("Recovery via SMS", f"{cost*0.35/1000:.1f}K EGP", "35% recovery est.", "up", "", "#34a853"),
        ], 3), unsafe_allow_html=True)
        info_card_end()

    # ── TAB 2: CHURN ──
    with tab2:
        if "churn_risk_category" in patients_data.columns:
            hi = patients_data[patients_data["churn_risk_category"]=="High Risk"]
            me = patients_data[patients_data["churn_risk_category"]=="Medium Risk"]
            lo = patients_data[patients_data["churn_risk_category"]=="Low Risk"]
        else:
            hi = me = lo = pd.DataFrame()
        n  = len(patients_data)

        st.markdown(kpi_row([
            kpi_card(" High Risk",   f"{len(hi):,}", f"{len(hi)/n*100:.1f}%" if n > 0 else "0%", "down",    "","#ea4335"),
            kpi_card("🟡 Medium Risk", f"{len(me):,}", f"{len(me)/n*100:.1f}%" if n > 0 else "0%", "neutral", "🟡","#fbbc04"),
            kpi_card("🟢 Low Risk",    f"{len(lo):,}", f"{len(lo)/n*100:.1f}%" if n > 0 else "0%", "up",      "🟢","#34a853")
        ], 3), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec_title(" Risk Level by Patient Tier",
                      "How each tier breaks down across risk categories")
            chart_start()
            if "churn_risk_category" in patients_data.columns and "patient_tier" in patients_data.columns:
                cross = (patients_data.groupby(["churn_risk_category","patient_tier"])
                         .size().reset_index(name="count"))
                fig = px.bar(
                    cross, x="churn_risk_category", y="count", color="patient_tier",
                    color_discrete_map={"Gold":"#fbbc04","Silver":"#9aa0a6","Bronze":"#cd7f32"},
                    barmode="group",
                    category_orders={"churn_risk_category":["Low Risk","Medium Risk","High Risk"]},
                    text="count"
                )
                fig.update_traces(textposition="outside", textfont_size=11)
                google_theme(fig, height=300)
                fig.update_layout(xaxis_title=None, yaxis_title="Patients", legend_title="Tier")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Required data not available")
            chart_end()

        with c2:
            sec_title(" Patient Engagement Status",
                      "Current engagement level across all patients")
            chart_start()
            if "engagement_status" in patients_data.columns:
                eng = patients_data["engagement_status"].value_counts().reset_index()
                eng.columns = ["Status", "Count"]
                color_map = {
                    "Highly Engaged": "#34a853",
                    "Engaged":        "#1a73e8",
                    "At Risk":        "#fbbc04",
                    "Inactive":       "#ea4335"
                }
                fig = px.bar(eng, x="Status", y="Count", color="Status",
                             color_discrete_map=color_map, text="Count")
                fig.update_traces(textposition="outside", textfont_size=12)
                google_theme(fig, height=300)
                fig.update_layout(xaxis_title=None, yaxis_title="Patients", showlegend=False)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Engagement status column not available in this dataset.")
            chart_end()

        sec_title(" Average Profile by Risk Category",
                  "What distinguishes high-risk patients from low-risk ones")
        chart_start()
        summary_cols = ["churn_risk_category", "total_visits",
                        "days_since_last_visit", "loyalty_points"]
        available    = [c for c in summary_cols if c in patients_data.columns]
        if len(available) > 1:
            summary = (patients_data[available]
                       .groupby("churn_risk_category")
                       .mean().round(1).reset_index())
            summary.columns = [c.replace("_"," ").title() for c in summary.columns]
            category_order  = ["Low Risk", "Medium Risk", "High Risk"]
            order_map       = {v: i for i, v in enumerate(category_order)}
            sort_col        = summary.columns[0]
            summary["_sort"] = summary[sort_col].map(order_map)
            summary = summary.sort_values("_sort").drop(columns=["_sort"])
            st.dataframe(summary, hide_index=True, use_container_width=True)
        chart_end()

        info_card_start(" Top 20 High-Risk Patients — Prioritise for Outreach")
        if len(hi) > 0:
            display_cols = [c for c in
                ["patient_id","churn_risk_score","days_since_last_visit",
                 "total_visits","loyalty_points","patient_tier"]
                if c in hi.columns]
            st.dataframe(hi.nlargest(20, "churn_risk_score")[display_cols] if "churn_risk_score" in hi.columns else hi[display_cols],
                        hide_index=True, use_container_width=True)
            st.download_button(" Export High-Risk List", export_to_excel(hi), "high_risk.xlsx")
        else:
            st.info("No high-risk patients found")
        info_card_end()

        # ── Feature 9: Patient Retention Cohort Table ──
        sec_title(" Monthly Acquisition Cohorts", "% of patients still active N months after first visit")
        chart_start()
        if "Visit_Date" in visits_data.columns:
            visits_data["cohort_month"] = visits_data.groupby("Patient_ID")["Visit_Date"].transform("min").dt.to_period("M")
            visits_data["visit_period"] = visits_data["Visit_Date"].dt.to_period("M")
            cohort_data = visits_data.groupby(["cohort_month","visit_period"])["Patient_ID"].nunique().reset_index()
            cohort_data["period_number"] = (cohort_data["visit_period"] - cohort_data["cohort_month"]).apply(lambda x: int(x.n))
            cohort_pivot = cohort_data.pivot(index="cohort_month", columns="period_number", values="Patient_ID")
            cohort_pct = cohort_pivot.divide(cohort_pivot[0], axis=0) * 100
            cohort_pct = cohort_pct.iloc[:, :12]
            # Convert Period index and numpy types to serializable Python types
            cohort_pct = cohort_pct.astype(float)
            cohort_pct.index = [str(p) for p in cohort_pct.index]
            cohort_pct.columns = [int(c) for c in cohort_pct.columns]
            fig = px.imshow(cohort_pct.round(1), color_continuous_scale="Blues",
                            labels=dict(x="Months Since First Visit", y="Cohort", color="Retention %"),
                            text_auto=".0f", aspect="auto")
            google_theme(fig, height=350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        chart_end()

        # ── ML Patient Segmentation ──
        sec_title(" ML Patient Segments",
                  "KMeans clustering identifies 5 distinct patient segments")
        chart_start()
        if len(patients_data) > 50:
            seg_df, seg_summary, seg_names = perform_patient_segmentation(patients_data)
            
            # Update summary with names
            seg_summary["segment_name"] = seg_summary["cluster"].map(seg_names)
            seg_summary = seg_summary.sort_values("count", ascending=False)
            
            c1, c2 = st.columns(2)
            with c1:
                # Cluster size donut
                fig = google_donut(
                    seg_summary["count"].values,
                    seg_summary["segment_name"].values,
                    ["#1a73e8", "#34a853", "#fbbc04", "#ea4335", "#9334e6"]
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
            with c2:
                # Segment characteristics
                display_summary = seg_summary[["segment_name", "count", "total_visits", "loyalty_points", "churn_risk_score"]].copy()
                display_summary.columns = ["Segment", "Count", "Avg Visits", "Avg Loyalty", "Avg Risk"]
                st.dataframe(display_summary, hide_index=True, use_container_width=True)
            
            # Cross-tab: Segment vs Tier
            if "patient_tier" in seg_df.columns:
                crosstab = pd.crosstab(seg_df["cluster"].map(seg_names), seg_df["patient_tier"])
                st.markdown("**Segment vs Tier Cross-Tabulation**")
                st.dataframe(crosstab, use_container_width=True)
        else:
            st.info("Need more patients for segmentation analysis")
        chart_end()

    # ── TAB 3: REVENUE + INFLATION + CAGR ──
    with tab3:
        INFL = 0.33
        mr = build_real_revenue(monthly_revenue, annual_inflation=INFL)
        if len(mr) < 2:
            st.info(" Building revenue analysis from visits data...")
            mr = build_real_revenue_from_visits(visits_data, annual_inflation=INFL)

        if len(mr) < 2:
            st.warning("️ Need ≥ 2 months of data to compute CAGR.")
        else:
            fd   = mr["visit_month"].iloc[0]
            ld   = mr["visit_month"].iloc[-1]
            span = max(1, (ld.year - fd.year)*12 + (ld.month - fd.month))
            nom0, nomF = mr["total_revenue"].iloc[0],  mr["total_revenue"].iloc[-1]
            re0,  reF  = mr["real_revenue"].iloc[0],   mr["real_revenue"].iloc[-1]
            cagr_nom  = compute_cagr(nom0, nomF, span)
            cagr_real = compute_cagr(re0,  reF,  span)
            gap       = cagr_nom - cagr_real
            total_nom  = mr["total_revenue"].sum()
            total_real = mr["real_revenue"].sum()
            total_tax  = mr["inflation_tax"].sum()

            st.markdown(kpi_row([
                kpi_card("Total Revenue (Nominal)", f"{total_nom/1e6:.2f}M EGP", "Actual EGP received",         "neutral","","#1a73e8"),
                kpi_card("Total Revenue (Real)",    f"{total_real/1e6:.2f}M EGP", "Base-month purchasing power", "neutral","","#34a853"),
                kpi_card("Inflation Erosion",       f"{total_tax/1e6:.2f}M EGP", f"Lost to {INFL*100:.0f}%/yr","down","","#ea4335"),
                kpi_card("Nominal CAGR",            f"{cagr_nom:+.1f}%",          f"Over {span} months",         "up" if cagr_nom>0 else "neutral","","#1a73e8"),
                kpi_card("Real CAGR",               f"{cagr_real:+.1f}%",          "After inflation",             "up" if cagr_real>0 else "down","",
                         "#34a853" if cagr_real>0 else "#ea4335"),
            ],5), unsafe_allow_html=True)

            st.info(f" **Inflation Note:** Real CAGR = **{cagr_real:+.1f}%** after Egypt's ~{INFL*100:.0f}%/yr inflation")

            # ── Chart 1: Nominal vs Real Revenue ──
            sec_title(" Nominal vs Real Revenue Over Time",
                      "Blue = actual EGP received | Green = inflation-adjusted purchasing power")
            chart_start()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["total_revenue"],
                mode="lines+markers", name="Nominal Revenue",
                line=dict(color="#1a73e8", width=3), marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["real_revenue"],
                mode="lines+markers", name="Real Revenue",
                line=dict(color="#34a853", width=3), marker=dict(size=8)
            ))
            # Fill the gap between nominal and real
            fig.add_trace(go.Scatter(
                x=list(mr["visit_month"]) + list(mr["visit_month"][::-1]),
                y=list(mr["total_revenue"]) + list(mr["real_revenue"][::-1]),
                fill="toself", fillcolor="rgba(234,67,53,0.15)",
                line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip",
                name="Inflation Erosion", showlegend=True
            ))
            google_theme(fig, height=350)
            fig.update_layout(
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="Revenue (EGP)",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            # ── Chart 2: Revenue Index Comparison ──
            sec_title(" Revenue Index — Nominal vs Real (Base = 100)",
                      "Shows how purchasing power erodes even when nominal numbers rise")
            chart_start()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["nominal_index"],
                mode="lines+markers", name="Nominal Index",
                line=dict(color="#1a73e8", width=3), marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["real_index"],
                mode="lines+markers", name="Real Index",
                line=dict(color="#34a853", width=3), marker=dict(size=8)
            ))
            fig.add_hline(y=100, line_dash="dash", line_color="#9aa0a6",
                         annotation_text="Base = 100", annotation_position="top right")
            google_theme(fig, height=320)
            fig.update_layout(
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="Index (Base = 100)",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            # ── Chart 3: Monthly Inflation Tax ──
            sec_title(" Monthly Inflation Erosion",
                      "How much revenue purchasing power is lost each month")
            chart_start()
            fig = px.bar(mr, x="visit_month", y="inflation_tax",
                        color="inflation_tax", color_continuous_scale="Reds",
                        text=mr["inflation_tax"].apply(lambda x: f"{x/1000:.0f}K"))
            fig.update_traces(textposition="outside")
            google_theme(fig, height=300)
            fig.update_layout(
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="EGP Lost to Inflation",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

    # ── TAB 4: PREDICTIVE TRENDS ──
    with tab4:
        # Use computed monthly metrics since monthly_trends table is empty
        forecast_metrics = monthly_metrics if len(monthly_metrics) > 1 else monthly_trends
        if len(forecast_metrics) > 1:
            predictions, std_err = predict_visits(forecast_metrics, months_ahead=3)
            historical = forecast_metrics[["visit_month","total_visits"]].copy()

            sec_title(" 3-Month Visit Forecast",
                      "Historical visits vs AI-predicted future visits (linear trend + confidence band)")
            chart_start()
            fig = go.Figure()
            upper_band = predictions["upper"].tolist()
            lower_band = predictions["lower"].tolist()
            band_x = predictions["visit_month"].tolist() + predictions["visit_month"].tolist()[::-1]
            band_y = upper_band + lower_band[::-1]
            fig.add_trace(go.Scatter(x=band_x, y=band_y, fill="toself",
                fillcolor="rgba(52,168,83,0.12)", line=dict(color="rgba(0,0,0,0)"),
                name="Confidence Range", hoverinfo="skip"))
            fig.add_trace(go.Scatter(x=historical["visit_month"], y=historical["total_visits"],
                name="Historical Visits", mode="lines+markers+text",
                line=dict(color="#1a73e8", width=3), marker=dict(size=10, color="#1a73e8"),
                text=[f"{v:,}" for v in historical["total_visits"]],
                textposition="top center", textfont=dict(size=10, color="#1a73e8")))
            fig.add_trace(go.Scatter(x=predictions["visit_month"], y=predictions["predicted_visits"],
                name="Predicted Visits", mode="lines+markers+text",
                line=dict(color="#34a853", width=3, dash="dash"),
                marker=dict(size=12, color="#34a853", symbol="diamond"),
                text=[f"{v:,}" for v in predictions["predicted_visits"]],
                textposition="top center", textfont=dict(size=10, color="#34a853")))
            safe_vline(fig, historical["visit_month"].max())
            google_theme(fig, height=420)
            fig.update_layout(yaxis_title="Number of Visits",
                              xaxis=dict(tickformat="%b %Y", dtick="M1",
                                         showgrid=False, showline=True, linecolor="#dadce0"),
                              hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            next_val   = int(predictions.iloc[0]["predicted_visits"])
            last_val   = int(historical.iloc[-1]["total_visits"])
            total_3m   = int(predictions["predicted_visits"].sum())
            avg_growth = (predictions["predicted_visits"].mean() / historical["total_visits"].mean() - 1) * 100

            st.markdown(kpi_row([
                kpi_card("Next Month Forecast", f"{next_val:,}",
                        f"{((next_val/last_val)-1)*100:+.1f}% vs last month",
                        "up" if next_val >= last_val else "down", "", "#1a73e8"),
                kpi_card("3-Month Total", f"{total_3m:,}", "predicted visits", "neutral", "", "#34a853"),
                kpi_card("Trend vs Avg", f"{avg_growth:+.1f}%", "vs historical avg",
                        "up" if avg_growth > 0 else "down", "",
                        "#34a853" if avg_growth > 0 else "#ea4335")
            ], 3), unsafe_allow_html=True)

            info_card_start(" Detailed Monthly Forecast")
            pred_display = predictions[["visit_month","predicted_visits","lower","upper"]].copy()
            pred_display["visit_month"] = pred_display["visit_month"].dt.strftime("%B %Y")
            pred_display.columns = ["Month", "Predicted Visits", "Lower Bound", "Upper Bound"]
            st.dataframe(pred_display, hide_index=True, use_container_width=True)
            info_card_end()

            st.info("""
**How to read this forecast:**
-  **Blue line** = actual historical visit data
- 🟢 **Green dashed line** = AI-predicted visits for next 3 months
- 🟩 **Green band** = confidence range (±1 standard deviation)
- **Vertical line** = divides past from future
- Model uses linear regression on historical trends — best used for short-term planning
            """)
        else:
            st.warning("Need at least 2 months of historical data for forecasting")

    # ── TAB 5: CLINICAL INSIGHTS ──
    with tab5:
        st.markdown(kpi_row([
            kpi_card("Diabetic Patients", 
                    f"{patients_data['Has_Diabetes'].sum() if 'Has_Diabetes' in patients_data.columns else 0:,}",
                    f"{(patients_data['Has_Diabetes'].sum()/len(patients_data)*100) if 'Has_Diabetes' in patients_data.columns and len(patients_data)>0 else 0:.1f}%",
                    "neutral", "", "#ea4335"),
            kpi_card("Hypertensive Patients",
                    f"{patients_data['Has_Hypertension'].sum() if 'Has_Hypertension' in patients_data.columns else 0:,}",
                    f"{(patients_data['Has_Hypertension'].sum()/len(patients_data)*100) if 'Has_Hypertension' in patients_data.columns and len(patients_data)>0 else 0:.1f}%",
                    "neutral", "️", "#fbbc04"),
            kpi_card("Dual Conditions",
                    f"{len(patients_data[(patients_data['Has_Diabetes']==1) & (patients_data['Has_Hypertension']==1)]) if 'Has_Diabetes' in patients_data.columns and 'Has_Hypertension' in patients_data.columns else 0:,}",
                    "comorbidity", "down", "️", "#9334e6"),
            kpi_card("High-Risk with Chronic",
                    f"{len(patients_data[(patients_data['churn_risk_category']=='High Risk') & ((patients_data['Has_Diabetes']==1) | (patients_data['Has_Hypertension']==1))]) if all(c in patients_data.columns for c in ['churn_risk_category','Has_Diabetes','Has_Hypertension']) else 0:,}",
                    "priority", "down", "", "#ea4335")
        ], 4), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec_title(" Diabetes Prevalence by Age Group")
            chart_start()
            if "Has_Diabetes" in patients_data.columns and "Age_Group" in patients_data.columns:
                diabetes_by_age = patients_data.groupby("Age_Group")["Has_Diabetes"].agg(["sum", "count"]).reset_index()
                diabetes_by_age["prevalence_pct"] = diabetes_by_age["sum"] / diabetes_by_age["count"] * 100
                fig = px.bar(diabetes_by_age, x="Age_Group", y="prevalence_pct",
                            color="prevalence_pct", color_continuous_scale="Reds",
                            text=diabetes_by_age["prevalence_pct"].round(1))
                fig.update_traces(textposition="outside", texttemplate="%{text:.1f}%")
                google_theme(fig, height=300)
                fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Prevalence %")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Clinical data not available")
            chart_end()

        with c2:
            sec_title("️ Hypertension Prevalence by Age Group")
            chart_start()
            if "Has_Hypertension" in patients_data.columns and "Age_Group" in patients_data.columns:
                ht_by_age = patients_data.groupby("Age_Group")["Has_Hypertension"].agg(["sum", "count"]).reset_index()
                ht_by_age["prevalence_pct"] = ht_by_age["sum"] / ht_by_age["count"] * 100
                fig = px.bar(ht_by_age, x="Age_Group", y="prevalence_pct",
                            color="prevalence_pct", color_continuous_scale="Oranges",
                            text=ht_by_age["prevalence_pct"].round(1))
                fig.update_traces(textposition="outside", texttemplate="%{text:.1f}%")
                google_theme(fig, height=300)
                fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Prevalence %")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Clinical data not available")
            chart_end()

        sec_title(" Comorbidity Heatmap",
                  "Patients with both Diabetes and Hypertension by Age Group and Gender")
        chart_start()
        if all(c in patients_data.columns for c in ["Has_Diabetes", "Has_Hypertension", "Age_Group", "Gender"]):
            patients_data["comorbidity"] = ((patients_data["Has_Diabetes"] == 1) & (patients_data["Has_Hypertension"] == 1)).astype(int)
            heatmap_data = patients_data.groupby(["Age_Group", "Gender"])["comorbidity"].sum().reset_index()
            heatmap_pivot = heatmap_data.pivot(index="Age_Group", columns="Gender", values="comorbidity").fillna(0)
            
            fig = px.imshow(heatmap_pivot, 
                          color_continuous_scale="Reds",
                          aspect="auto")
            google_theme(fig, height=300)
            fig.update_layout(xaxis_title="Gender", yaxis_title="Age Group")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Need clinical and demographic data for comorbidity analysis")
        chart_end()

        sec_title("️ Clinical Risk Factor Analysis",
                  "Average churn risk score by chronic condition status")
        chart_start()
        if "churn_risk_score" in patients_data.columns and "Has_Diabetes" in patients_data.columns:
            clinical_risk = []
            mask_diabetic = patients_data["Has_Diabetes"] == 1
            mask_hypertensive = patients_data["Has_Hypertension"] == 1 if "Has_Hypertension" in patients_data.columns else pd.Series(False, index=patients_data.index)
            
            clinical_risk.append({
                "Group": "Diabetic",
                "Avg Risk": patients_data.loc[mask_diabetic, "churn_risk_score"].mean(),
                "Count": mask_diabetic.sum()
            })
            clinical_risk.append({
                "Group": "Non-Diabetic",
                "Avg Risk": patients_data.loc[~mask_diabetic, "churn_risk_score"].mean(),
                "Count": (~mask_diabetic).sum()
            })
            if "Has_Hypertension" in patients_data.columns:
                clinical_risk.append({
                    "Group": "Hypertensive",
                    "Avg Risk": patients_data.loc[mask_hypertensive, "churn_risk_score"].mean(),
                    "Count": mask_hypertensive.sum()
                })
                clinical_risk.append({
                    "Group": "Non-Hypertensive",
                    "Avg Risk": patients_data.loc[~mask_hypertensive, "churn_risk_score"].mean(),
                    "Count": (~mask_hypertensive).sum()
                })
            
            risk_df = pd.DataFrame(clinical_risk)
            risk_df = risk_df.dropna()
            if not risk_df.empty:
                fig = px.bar(risk_df, x="Group", y="Avg Risk", color="Avg Risk",
                            color_continuous_scale="RdYlGn_r", text=risk_df["Avg Risk"].round(1))
                fig.update_traces(textposition="outside")
                google_theme(fig, height=300)
                fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Avg Churn Risk")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.dataframe(risk_df.round(1), hide_index=True, use_container_width=True)
        else:
            st.info("Need churn risk and clinical data for analysis")
        chart_end()

    # ── TAB 6: DATA QUALITY ──
    with tab6:
        sec_title(" Data Quality Dashboard",
                  "Monitor data completeness, freshness, and integrity across all tables")
        
        # Compute quality for all tables
        quality_metrics = []
        for df, name in [(patients_data, "Patients"), (visits_data, "Visits"), 
                         (doctors_data, "Doctors"), (corporates_data, "Corporates"),
                         (branches_data, "Branches")]:
            quality_metrics.append(compute_data_quality(df, name))
        
        quality_df = pd.DataFrame(quality_metrics)
        
        st.markdown(kpi_row([
            kpi_card("Overall Score", 
                    f"{quality_df['completeness_score'].mean():.1f}%",
                    "avg completeness", "up" if quality_df['completeness_score'].mean() > 90 else "neutral",
                    "", "#1a73e8"),
            kpi_card("Total Records",
                    f"{quality_df['total_rows'].sum():,}",
                    "across all tables", "neutral", "️", "#34a853"),
            kpi_card("Missing Cells",
                    f"{quality_df['missing_pct'].mean():.1f}%",
                    "avg missing rate", "down" if quality_df['missing_pct'].mean() > 5 else "up",
                    "️", "#ea4335" if quality_df['missing_pct'].mean() > 5 else "#34a853"),
            kpi_card("Duplicates",
                    f"{quality_df['duplicate_rows'].sum():,}",
                    "total duplicates", "neutral", "", "#fbbc04")
        ], 4), unsafe_allow_html=True)

        chart_start()
        fig = px.bar(quality_df, x="table", y="completeness_score",
                    color="completeness_score", color_continuous_scale="RdYlGn",
                    text=quality_df["completeness_score"].round(1))
        fig.update_traces(textposition="outside", texttemplate="%{text:.1f}%")
        fig.add_hline(y=90, line_dash="dash", line_color="#ea4335",
                     annotation_text="Target: 90%")
        google_theme(fig, height=300)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Completeness %")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        chart_end()

        info_card_start("Detailed Quality Report")
        display_quality = quality_df.copy()
        display_quality.columns = ["Table", "Rows", "Columns", "Missing %", "Duplicates", "Score"]
        st.dataframe(display_quality, hide_index=True, use_container_width=True)
        info_card_end()

        # Per-table missing value analysis
        st.markdown("#### Missing Values by Column")
        selected_table = st.selectbox("Select table", ["Patients", "Visits", "Doctors", "Corporates", "Branches"])
        table_map = {
            "Patients": patients_data, "Visits": visits_data,
            "Doctors": doctors_data, "Corporates": corporates_data,
            "Branches": branches_data
        }
        selected_df = table_map.get(selected_table, pd.DataFrame())
        if not selected_df.empty:
            missing_by_col = selected_df.isna().sum()
            missing_pct = (missing_by_col / len(selected_df) * 100).round(1)
            missing_report = pd.DataFrame({
                "Column": missing_by_col.index,
                "Missing Count": missing_by_col.values,
                "Missing %": missing_pct.values
            })
            missing_report = missing_report[missing_report["Missing Count"] > 0]
            if not missing_report.empty:
                st.dataframe(missing_report.sort_values("Missing %", ascending=False), 
                           hide_index=True, use_container_width=True)
            else:
                st.success(" No missing values in this table!")


    # ── TAB 7: BRANCH OPERATIONAL SCORECARD (Feature 6) ──
    with tab7:
        sec_title("📊 Branch Operational Scorecard", "Performance metrics across all branches")
        try:
            if "Branch_Name" in filtered_visits.columns and len(filtered_visits) > 0:
                # Build aggregation dict only for columns that exist
                agg_dict = {}
                if "Visit_ID" in filtered_visits.columns:
                    agg_dict["total_visits"] = ("Visit_ID", "count")
                if "Patient_ID" in filtered_visits.columns:
                    agg_dict["unique_patients"] = ("Patient_ID", "nunique")
                if "Visit_Duration" in filtered_visits.columns:
                    agg_dict["avg_duration"] = ("Visit_Duration", "mean")
                if "Is_Weekend" in filtered_visits.columns:
                    agg_dict["weekend_visits"] = ("Is_Weekend", "sum")
                if "Is_Peak_Hour" in filtered_visits.columns:
                    agg_dict["peak_visits"] = ("Is_Peak_Hour", "sum")
                if "Amount_Paid" in filtered_visits.columns:
                    agg_dict["revenue"] = ("Amount_Paid", "sum")

                if not agg_dict or len(agg_dict) < 2:
                    st.warning("⚠️ Insufficient data: Need Visit_ID and Amount_Paid columns. Checking database...")
                else:
                    branch_ops = filtered_visits.groupby("Branch_Name").agg(**agg_dict).reset_index()

                    # Compute derived metrics only if base columns exist
                    if "weekend_visits" in branch_ops.columns and "total_visits" in branch_ops.columns:
                        branch_ops["weekend_pct"] = (branch_ops["weekend_visits"] / branch_ops["total_visits"] * 100).round(1)
                    if "peak_visits" in branch_ops.columns and "total_visits" in branch_ops.columns:
                        branch_ops["peak_pct"] = (branch_ops["peak_visits"] / branch_ops["total_visits"] * 100).round(1)
                    if "revenue" in branch_ops.columns and "total_visits" in branch_ops.columns:
                        branch_ops["revenue_per_visit"] = (branch_ops["revenue"] / branch_ops["total_visits"]).round(0)

                    total_branches = len(branch_ops)
                    top_branch_visits = branch_ops.loc[branch_ops["total_visits"].idxmax(), "Branch_Name"] if total_branches > 0 and "total_visits" in branch_ops.columns else "N/A"
                    top_branch_revenue = branch_ops.loc[branch_ops["revenue"].idxmax(), "Branch_Name"] if total_branches > 0 and "revenue" in branch_ops.columns else "N/A"
                    avg_rev_visit = branch_ops["revenue_per_visit"].mean() if total_branches > 0 and "revenue_per_visit" in branch_ops.columns else 0

                    # Debug info
                    if total_branches == 0:
                        st.warning("No branch data available for the selected date range")
                    elif "total_visits" not in branch_ops.columns:
                        st.error("Visit data not available for branch analysis. Please verify database.")

                st.markdown(kpi_row([
                            kpi_card("Total Branches", str(total_branches), "", "neutral", "", "#1a73e8"),
                            kpi_card("Top by Visits", str(top_branch_visits), "", "up", "", "#34a853"),
                            kpi_card("Top by Revenue", str(top_branch_revenue), "", "up", "", "#fbbc04"),
                            kpi_card("Avg Rev/Visit", f"{avg_rev_visit:,.0f} EGP", "", "neutral", "", "#9334e6"),
                        ], 4), unsafe_allow_html=True)
                # Only show charts if we have the necessary columns
                if "total_visits" in branch_ops.columns:
                    sec_title(" Visits vs Revenue per Visit by Branch")
                    chart_start()
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=branch_ops["Branch_Name"], y=branch_ops["total_visits"],
                                         name="Total Visits", marker_color="#1a73e8", yaxis="y"))
                    if "revenue_per_visit" in branch_ops.columns:
                        fig.add_trace(go.Scatter(x=branch_ops["Branch_Name"], y=branch_ops["revenue_per_visit"],
                                                 name="Rev/Visit", mode="lines+markers", marker_color="#34a853", yaxis="y2"))
                    fig.update_layout(
                        yaxis=dict(title="Total Visits", side="left"),
                        yaxis2=dict(title="Revenue/Visit (EGP)", overlaying="y", side="right") if "revenue_per_visit" in branch_ops.columns else {},
                        legend=dict(orientation="h", yanchor="bottom", y=1.02),
                        height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                    )
                    google_theme(fig, height=350)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                    chart_end()

                # Radar chart
                radar_metrics = []
                if "total_visits" in branch_ops.columns:
                    radar_metrics.append("total_visits")
                if "revenue" in branch_ops.columns:
                    radar_metrics.append("revenue")
                if "unique_patients" in branch_ops.columns:
                    radar_metrics.append("unique_patients")
                if "peak_pct" in branch_ops.columns:
                    radar_metrics.append("peak_pct")
                if "weekend_pct" in branch_ops.columns:
                    radar_metrics.append("weekend_pct")

                if len(radar_metrics) >= 3:
                    sec_title("️ Branch Performance Radar")
                    chart_start()
                    radar_df = branch_ops.copy()
                    for m in radar_metrics:
                        max_val = radar_df[m].max()
                        radar_df[m + "_norm"] = (radar_df[m] / max_val * 100).round(1) if max_val > 0 else 0

                    fig = go.Figure()
                    for _, row in radar_df.iterrows():
                        fig.add_trace(go.Scatterpolar(
                            r=[row[m + "_norm"] for m in radar_metrics] + [row[radar_metrics[0] + "_norm"]],
                            theta=[m.replace("_", " ").title() for m in radar_metrics] + [radar_metrics[0].replace("_", " ").title()],
                            fill="toself", name=row["Branch_Name"], opacity=0.3
                        ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                        height=450, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                    chart_end()

                info_card_start(" Branch Scorecard Table")
                st.dataframe(branch_ops.sort_values("total_visits", ascending=False) if "total_visits" in branch_ops.columns else branch_ops,
                             hide_index=True, use_container_width=True)
                st.download_button(" Export Branch Scorecard", export_to_excel(branch_ops), "branch_scorecard.xlsx")
                info_card_end()
        else:
            st.info("Branch_Name column not available in visits data")

    # ── TAB 8: REVENUE MIX (Feature 8) ──
    with tab8:
        sec_title("💰 Revenue Per Patient Tier", "Which tier delivers the most value?")
        # Filter visits by date range and check for required columns
        tier_visits = filtered_visits if "patient_tier" in filtered_visits.columns and "Amount_Paid" in filtered_visits.columns else None
        
        if tier_visits is not None and len(tier_visits) > 0:
            try:
                tier_revenue = tier_visits.groupby("patient_tier").agg(
                    total_revenue=("Amount_Paid","sum"),
                    visit_count=("Visit_ID" if "Visit_ID" in tier_visits.columns else "patient_tier","count"),
                    unique_patients=("Patient_ID" if "Patient_ID" in tier_visits.columns else "patient_tier","nunique")
                ).reset_index()
                tier_revenue["revenue_per_patient"] = (tier_revenue["total_revenue"] / tier_revenue["unique_patients"].clip(lower=1)).round(0)
                tier_revenue["revenue_per_visit"] = (tier_revenue["total_revenue"] / tier_revenue["visit_count"].clip(lower=1)).round(0)
                tier_revenue["revenue_share_pct"] = (tier_revenue["total_revenue"] / tier_revenue["total_revenue"].sum() * 100).round(1)

                gold_val = tier_revenue[tier_revenue['patient_tier']=='Gold']['revenue_per_patient'].values
                silver_val = tier_revenue[tier_revenue['patient_tier']=='Silver']['revenue_per_patient'].values
                bronze_val = tier_revenue[tier_revenue['patient_tier']=='Bronze']['revenue_per_patient'].values

                st.markdown(kpi_row([
                    kpi_card("Gold Rev/Patient", f"{gold_val[0]:,.0f}" if len(gold_val) > 0 else "N/A", "", "neutral", "✨", "#fbbc04"),
                    kpi_card("Silver Rev/Patient", f"{silver_val[0]:,.0f}" if len(silver_val) > 0 else "N/A", "", "neutral", "⭐", "#9aa0a6"),
                    kpi_card("Bronze Rev/Patient", f"{bronze_val[0]:,.0f}" if len(bronze_val) > 0 else "N/A", "", "neutral", "🥉", "#cd7f32"),
                ], 3), unsafe_allow_html=True)

                sec_title("💹 Revenue Share by Tier")
                chart_start()
                fig = px.bar(tier_revenue, x="patient_tier", y="total_revenue",
                             color="patient_tier", text="revenue_share_pct",
                             color_discrete_map={"Gold":"#fbbc04","Silver":"#9aa0a6","Bronze":"#cd7f32"})
                fig.update_traces(texttemplate="%{text}%", textposition="outside")
                google_theme(fig, height=300)
                fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Revenue (EGP)")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                chart_end()

                sec_title("👥 Patients vs Revenue by Tier")
                chart_start()
                fig = px.scatter(tier_revenue, x="unique_patients", y="total_revenue",
                                 color="patient_tier", size="revenue_per_patient",
                                 color_discrete_map={"Gold":"#fbbc04","Silver":"#9aa0a6","Bronze":"#cd7f32"},
                                 text="patient_tier")
                fig.update_traces(textposition="top center")
                google_theme(fig, height=300)
                fig.update_layout(xaxis_title="Unique Patients", yaxis_title="Total Revenue (EGP)")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                chart_end()

                info_card_start("📊 Tier Metrics Table")
                st.dataframe(tier_revenue.sort_values("total_revenue", ascending=False),
                             hide_index=True, use_container_width=True)
                st.download_button("📥 Export Tier Analysis", export_to_excel(tier_revenue), "tier_revenue.xlsx")
                info_card_end()
            except Exception as e:
                st.error(f"Error processing tier data: {str(e)}")
        else:
            st.warning("⚠️ Amount_Paid or patient_tier columns not available in visit data")
            except Exception as e:
                st.error(f"Error processing tier data: {str(e)}")
        else:
            st.warning("Amount_Paid or patient_tier columns not available in visit data. Running database rebuild...")

    # ── TAB 9: BRANCH VS BRANCH COMPARISON ──
    with tab9:
        sec_title("⚔️ Branch vs Branch Comparison", "Head-to-head performance analysis")
        if "Branch_Name" in filtered_visits.columns:
            branches_list = sorted(filtered_visits["Branch_Name"].unique().tolist())
            if len(branches_list) >= 2:
                c1, c2 = st.columns(2)
                with c1:
                    branch_a = st.selectbox(" Branch A", branches_list, index=0, key="branch_a")
                with c2:
                    branch_b = st.selectbox(" Branch B", branches_list, index=min(1, len(branches_list)-1), key="branch_b")

                # Compute metrics dynamically based on available columns
                agg_dict = {}
                if "Visit_ID" in filtered_visits.columns:
                    agg_dict["total_visits"] = ("Visit_ID", "count")
                if "Patient_ID" in filtered_visits.columns:
                    agg_dict["unique_patients"] = ("Patient_ID", "nunique")
                if "Amount_Paid" in filtered_visits.columns:
                    agg_dict["revenue"] = ("Amount_Paid", "sum")
                if "Visit_Duration" in filtered_visits.columns:
                    agg_dict["avg_duration"] = ("Visit_Duration", "mean")

                if agg_dict:
                    bm = filtered_visits.groupby("Branch_Name").agg(**agg_dict).reset_index()
                    if "revenue" in bm.columns and "total_visits" in bm.columns:
                        bm["revenue_per_visit"] = (bm["revenue"] / bm["total_visits"]).round(0)

                    a_row = bm[bm["Branch_Name"] == branch_a]
                    b_row = bm[bm["Branch_Name"] == branch_b]
                    a_data = a_row.iloc[0] if not a_row.empty else None
                    b_data = b_row.iloc[0] if not b_row.empty else None

                    if a_data is not None and b_data is not None:
                        # Comparison KPI row
                        def diff_card(label, col, icon, accent_a, accent_b):
                            a_val = int(a_data[col]) if col in a_data.index else 0
                            b_val = int(b_data[col]) if col in b_data.index else 0
                            diff = a_val - b_val
                            if diff > 0:
                                return kpi_card(f"{label} (A)", f"{a_val:,}", f"+{diff:,} vs B", "up", icon, accent_a)
                            elif diff < 0:
                                return kpi_card(f"{label} (A)", f"{a_val:,}", f"{diff:,} vs B", "down", icon, accent_a)
                            else:
                                return kpi_card(f"{label} (A)", f"{a_val:,}", "Tied with B", "neutral", icon, "#fbbc04")

                        cards = []
                        if "total_visits" in bm.columns:
                            cards.append(diff_card("Visits", "total_visits", "", "#1a73e8", "#ea4335"))
                        if "unique_patients" in bm.columns:
                            cards.append(diff_card("Patients", "unique_patients", "", "#34a853", "#ea4335"))
                        if "revenue" in bm.columns:
                            a_rev = int(a_data["revenue"]) if "revenue" in a_data.index else 0
                            b_rev = int(b_data["revenue"]) if "revenue" in b_data.index else 0
                            diff_rev = a_rev - b_rev
                            trend = "up" if diff_rev > 0 else "down" if diff_rev < 0 else "neutral"
                            cards.append(kpi_card("Revenue A", f"{a_rev/1000:.1f}K", f"{diff_rev/1000:+.1f}K vs B", trend, "", "#9334e6"))
                        if "revenue_per_visit" in bm.columns:
                            a_rpv = int(a_data["revenue_per_visit"]) if "revenue_per_visit" in a_data.index else 0
                            b_rpv = int(b_data["revenue_per_visit"]) if "revenue_per_visit" in b_data.index else 0
                            diff_rpv = a_rpv - b_rpv
                            trend = "up" if diff_rpv > 0 else "down" if diff_rpv < 0 else "neutral"
                            cards.append(kpi_card("Rev/Visit A", f"{a_rpv:,}", f"{diff_rpv:+,} vs B", trend, "", "#fbbc04"))
                        if "avg_duration" in bm.columns:
                            a_dur = int(a_data["avg_duration"]) if "avg_duration" in a_data.index else 0
                            b_dur = int(b_data["avg_duration"]) if "avg_duration" in b_data.index else 0
                            diff_dur = a_dur - b_dur
                            trend = "up" if diff_dur > 0 else "down" if diff_dur < 0 else "neutral"
                            cards.append(kpi_card("Duration A", f"{a_dur} min", f"{diff_dur:+,} vs B", trend, "⏱️", "#1a73e8"))

                        if cards:
                            st.markdown(kpi_row(cards, cols=len(cards)), unsafe_allow_html=True)

                        # Grouped bar chart comparison
                        sec_title("📊 Side-by-Side Comparison", "Key metrics across selected branches")
                        chart_start()
                        compare_cols = [c for c in ["total_visits", "unique_patients", "revenue", "revenue_per_visit"] if c in bm.columns]
                        if compare_cols:
                            compare_df = bm[bm["Branch_Name"].isin([branch_a, branch_b])].copy()
                            # Melt for grouped bar chart
                            melted = compare_df.melt(id_vars=["Branch_Name"], value_vars=compare_cols,
                                                     var_name="Metric", value_name="Value")
                            metric_labels = {
                                "total_visits": "Total Visits",
                                "unique_patients": "Unique Patients",
                                "revenue": "Revenue",
                                "revenue_per_visit": "Rev/Visit"
                            }
                            melted["Metric"] = melted["Metric"].map(metric_labels)
                            fig = px.bar(melted, x="Metric", y="Value", color="Branch_Name",
                                         barmode="group", color_discrete_map={branch_a: "#1a73e8", branch_b: "#34a853"},
                                         text="Value")
                            fig.update_traces(textposition="outside")
                            google_theme(fig, height=350)
                            fig.update_layout(xaxis_title=None, yaxis_title="Value",
                                              legend=dict(orientation="h", yanchor="bottom", y=1.02))
                            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        chart_end()

                        # Difference table
                        info_card_start("📋 Metric Comparison Table")
                        diff_data = []
                        for col in compare_cols:
                            a_v = a_data[col] if col in a_data.index else 0
                            b_v = b_data[col] if col in b_data.index else 0
                            label = metric_labels.get(col, col)
                            diff_data.append({
                                "Metric": label,
                                f"{branch_a}": f"{a_v:,.0f}",
                                f"{branch_b}": f"{b_v:,.0f}",
                                "Difference": f"{a_v - b_v:+,}",
                                "Winner": "A" if a_v > b_v else "B" if b_v > a_v else "Tie"
                            })
                        diff_df = pd.DataFrame(diff_data)
                        st.dataframe(diff_df, hide_index=True, use_container_width=True)
                        info_card_end()
                    else:
                        st.warning("Could not retrieve data for one or both branches")
                else:
                    st.info("No aggregatable columns available for comparison")
            else:
                st.info("Need at least 2 branches to compare")
        else:
            st.info("Branch_Name column not available in visits data")

# ============================================================
# PAGE: EXPORT
# ============================================================

elif page == "  Export":
    st.markdown("""<div class="page-header">
<h1>Export Data</h1>
<p>Download analytics data for external use</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]

    table_options = {
        "Patients":           "patients",
        "Doctors":            "doctors",
        "Corporate Contracts":"corporates",
        "Branches":           "branches",
        "High Risk Patients": "high_risk"
    }

    selected = st.selectbox("Select table to export", list(table_options.keys()))

    if selected == "High Risk Patients":
        if "churn_risk_category" in patients_data.columns:
            export_data = patients_data[patients_data["churn_risk_category"] == "High Risk"]
        else:
            export_data = patients_data
    else:
        try:
            export_data = pd.read_sql(f"SELECT * FROM {table_options[selected]}", conn)
        except:
            export_data = pd.DataFrame()

    info_card_start(f"Preview: {selected}")
    st.markdown(f'<p style="color:#5f6368;font-size:.85rem">Total records: {len(export_data):,}</p>',
                unsafe_allow_html=True)
    st.dataframe(export_data.head(10), hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(" Download as Excel",
                          export_to_excel(export_data),
                          f"{selected.lower().replace(' ', '_')}.xlsx",
                          use_container_width=True)
    with c2:
        st.download_button(" Download as CSV",
                          export_to_csv(export_data),
                          f"{selected.lower().replace(' ', '_')}.csv",
                          use_container_width=True)
    info_card_end()

# ============================================================
# PAGE: REPORTS
# ============================================================

elif page == " Reports":
    st.markdown("""<div class="page-header">
<h1>Reports & Exports</h1>
<p>Generate and download comprehensive analytics reports</p>
</div>""", unsafe_allow_html=True)

    # Global date filter
    date_start = st.session_state.get("date_start", visits_data["Visit_Date"].min())
    date_end   = st.session_state.get("date_end",   visits_data["Visit_Date"].max())
    filtered_visits = visits_data[(visits_data["Visit_Date"] >= date_start) & (visits_data["Visit_Date"] <= date_end)]
    
    # Phase 4: Report generation UI
    tab1, tab2 = st.tabs([" Full Report", "️ Custom Report"])
    
    with tab1:
        sec_title(" Executive Summary Report")
        st.markdown('<p style="color:#5f6368">Comprehensive report with all tables</p>',
                   unsafe_allow_html=True)
        
        if st.button(" Generate Full Report", type="primary", use_container_width=True):
            with st.spinner("Building report..."):
                report_bytes = build_report_excel(
                    patients_data, visits_data, branches_data,
                    doctors_data, corporates_data
                )
                st.success(" Report generated successfully!")
                st.download_button(
                    " Download Excel Report",
                    report_bytes,
                    format_report_filename("full"),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    with tab2:
        sec_title("️ Custom Report Builder")
        st.markdown('<p style="color:#5f6368">Select data sources to include</p>',
                   unsafe_allow_html=True)
        
        include_patients = st.checkbox("Patients", value=True)
        include_visits = st.checkbox("Visits", value=True)
        include_branches = st.checkbox("Branches", value=True)
        include_doctors = st.checkbox("Doctors", value=False)
        include_corporates = st.checkbox("Corporate Contracts", value=False)
        
        if st.button(" Build Custom Report", type="primary", use_container_width=True):
            with st.spinner("Building custom report..."):
                selected = {}
                if include_patients: selected["Patients"] = patients_data
                if include_visits: selected["Visits"] = visits_data
                if include_branches: selected["Branches"] = branches_data
                if include_doctors: selected["Doctors"] = doctors_data
                if include_corporates: selected["Corporates"] = corporates_data
                
                if selected:
                    report_bytes = build_custom_report(selected)
                    st.success(f" Custom report generated with {len(selected)} sheets!")
                    st.download_button(
                        " Download Custom Report",
                        report_bytes,
                        format_report_filename("custom"),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.warning("Please select at least one data source")

    # ── Feature 10: PDF Report Export (admin-only) ──
    if is_admin():
        st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                    unsafe_allow_html=True)
        pdf_bytes = build_report_pdf(patients_data, visits_data, branches_data)
        st.download_button(" Download PDF Report", pdf_bytes,
                           format_report_filename("executive").replace(".xlsx", ".pdf"),
                           mime="application/pdf", use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown(f"""
<div style="text-align:center; margin-top:3rem; padding:1.5rem 0;
     border-top:1px solid #dadce0; color:#5f6368; font-size:0.8125rem;
     font-family:'Google Sans',sans-serif; line-height:1.8;">
  <div style="font-weight:600; color:#202124; font-size:0.875rem; margin-bottom:4px;">
    Trust Labs Healthcare Analytics &nbsp;·&nbsp; v3.0
  </div>
  <div>
    Data Analysis for Health Care Systems &nbsp;·&nbsp;
    <strong>Ahmed Mustafa</strong>
  </div>
  <div style="margin-top:4px;">
     <a href="https://wa.me/201143575727" style="color:#1a73e8;text-decoration:none;">01143575727</a>
    &nbsp;&nbsp;
     <a href="mailto:ahmdsa1@proton.com" style="color:#1a73e8;text-decoration:none;">ahmdsa1@proton.com</a>
  </div>
  <div style="margin-top:6px; color:#9aa0a6; font-size:0.75rem;">
    Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M")}
  </div>
</div>
""", unsafe_allow_html=True)

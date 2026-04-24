"""
Trust Labs - Professional Analytics Dashboard
Complete system with churn prediction, points, and analytics
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page config
st.set_page_config(
    page_title="Trust Labs Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-good {color: #28a745;}
    .metric-warning {color: #ffc107;}
    .metric-danger {color: #dc3545;}
    h1 {color: #2c3e50;}
    h2 {color: #34495e;}
    h3 {color: #7f8c8d;}
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect('trust_labs.db', check_same_thread=False)

conn = get_connection()

# Load data functions
@st.cache_data(ttl=300)
def load_patients():
    return pd.read_sql('SELECT * FROM patients', conn)

@st.cache_data(ttl=300)
def load_visits():
    return pd.read_sql('SELECT * FROM visits', conn)

@st.cache_data(ttl=300)
def load_branches():
    return pd.read_sql('SELECT * FROM branches', conn)

# Helper functions
def format_number(num):
    """Format numbers with commas"""
    return f"{num:,}"

def get_risk_color(score):
    """Get color based on risk score"""
    if score < 30:
        return "🟢"
    elif score < 60:
        return "🟡"
    else:
        return "🔴"

def get_tier_emoji(tier):
    """Get emoji for patient tier"""
    if tier == 'Gold':
        return "🥇"
    elif tier == 'Silver':
        return "🥈"
    else:
        return "🥉"

# Load all data
patients = load_patients()
visits = load_visits()
branches = load_branches()

# ============================================
# SIDEBAR NAVIGATION
# ============================================

with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=Trust+Labs", use_container_width=True)
    st.markdown("---")
    
    page = st.radio(
        "🧭 Navigate",
        [
            "📊 Executive Dashboard",
            "🔍 Patient Lookup",
            "⚠️ Churn Analysis",
            "⭐ Loyalty & Points",
            "🏢 Branch Performance",
            "📈 Analytics & Trends",
            "📥 Export Reports"
        ]
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Patients", format_number(len(patients)))
    st.metric("Total Visits", format_number(len(visits)))
    st.metric("Active Branches", len(branches))
    
    high_risk_patients = len(patients[patients['churn_risk_score'] >= 60])
    st.metric("High Risk Patients", format_number(high_risk_patients), 
              delta=f"-{high_risk_patients}", delta_color="inverse")

# ============================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================

if page == "📊 Executive Dashboard":
    st.title("📊 Trust Labs Executive Dashboard")
    st.markdown("### Real-time performance overview")
    
    # Top KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Patients",
            format_number(len(patients)),
            delta="+2.5%",
            help="Total unique patients in system"
        )
    
    with col2:
        st.metric(
            "Total Visits",
            format_number(len(visits)),
            delta="+5.8%",
            help="All patient visits recorded"
        )
    
    with col3:
        avg_visits = len(visits) / len(patients)
        st.metric(
            "Avg Visits/Patient",
            f"{avg_visits:.1f}",
            delta="+0.3",
            help="Average number of visits per patient"
        )
    
    with col4:
        diabetes_pct = (patients['Has_Diabetes'].sum() / len(patients) * 100)
        st.metric(
            "Diabetes Rate",
            f"{diabetes_pct:.1f}%",
            delta="-0.5%",
            delta_color="inverse",
            help="Percentage of patients with diabetes"
        )
    
    with col5:
        high_risk_pct = (high_risk_patients / len(patients) * 100)
        st.metric(
            "Churn Risk",
            f"{high_risk_pct:.1f}%",
            delta="+1.2%",
            delta_color="inverse",
            help="Patients at high risk of churning"
        )
    
    st.markdown("---")
    
    # Row 2: Patient & Visit trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Patient Demographics")
        
        # Gender distribution
        gender_counts = patients['Gender'].value_counts()
        fig = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📅 Monthly Visit Trend")
        
        # Visits by month
        month_visits = visits.groupby('Visit_Month').size().reset_index(name='Visits')
        fig = px.line(
            month_visits,
            x='Visit_Month',
            y='Visits',
            markers=True,
            title="Visit Volume Over Time"
        )
        fig.update_traces(line_color='#667eea', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Branch & Risk Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏢 Top 5 Branches by Volume")
        
        top_branches = branches.nlargest(5, 'total_visits')
        fig = px.bar(
            top_branches,
            x='total_visits',
            y='Branch_Name',
            orientation='h',
            text='total_visits',
            color='performance_score',
            color_continuous_scale='RdYlGn'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### ⚠️ Churn Risk Distribution")
        
        risk_counts = patients['churn_risk_category'].value_counts()
        colors = ['#28a745', '#ffc107', '#dc3545']
        fig = go.F
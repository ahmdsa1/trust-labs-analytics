"""
Trust Labs Alert System
Monitors high-risk patients and generates alert banners.
"""

import pandas as pd
import streamlit as st
from datetime import datetime


def get_high_risk_alerts(patients_df: pd.DataFrame, risk_threshold: int = 80) -> pd.DataFrame:
    """
    Identify patients who need immediate attention.
    Criteria: churn_risk_score >= risk_threshold AND not already flagged.
    """
    if patients_df.empty or "churn_risk_score" not in patients_df.columns:
        return pd.DataFrame()
    
    alerts = patients_df[
        (patients_df["churn_risk_score"] >= risk_threshold)
    ].copy()
    
    # Sort by risk score descending
    alerts = alerts.sort_values("churn_risk_score", ascending=False)
    
    # Select display columns
    cols = ["Patient_ID", "Age_Group", "Gender", "churn_risk_score", 
            "churn_risk_category", "total_visits", "days_since_last_visit"]
    available = [c for c in cols if c in alerts.columns]
    return alerts[available].head(10)


def render_alert_banner(patients_df: pd.DataFrame):
    """Render a collapsible alert banner for high-risk patients."""
    alerts = get_high_risk_alerts(patients_df)
    count = len(alerts)
    
    if count == 0:
        return
    
    # Alert banner styling
    st.markdown(f"""
    <div style="background:#fce8e8;border-left:4px solid #ea4335;
                padding:12px 16px;border-radius:8px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:1.2rem;">🚨</span>
            <div>
                <div style="font-weight:600;color:#202124;font-size:0.95rem;">
                    {count} High-Risk Patient{"s" if count > 1 else ""} Detected
                </div>
                <div style="color:#5f6368;font-size:0.8rem;">
                    Churn risk score ≥ 80 — immediate attention recommended
                </div>
        </div>
    """, unsafe_allow_html=True)


def render_alert_table(patients_df: pd.DataFrame):
    """Render detailed alert table in an expander."""
    alerts = get_high_risk_alerts(patients_df)
    
    if alerts.empty:
        st.info("No high-risk patients detected. Great job!")
        return
    
    with st.expander(f"🔍 View {len(alerts)} High-Risk Patients", expanded=False):
        # Color-code risk scores
        def color_risk(val):
            if pd.isna(val):
                return ""
            if val >= 90:
                return "background-color:#fce8e8;color:#ea4335;font-weight:600"
            elif val >= 80:
                return "background-color:#fef3e8;color:#f9ab00;font-weight:600"
            return ""
        
        styled = alerts.style.applymap(color_risk, subset=["churn_risk_score"])
        st.dataframe(styled, hide_index=True, use_container_width=True, height=300)


def get_alert_summary(patients_df: pd.DataFrame) -> dict:
    """Get summary statistics for alerts dashboard."""
    if patients_df.empty:
        return {"total_alerts": 0, "critical": 0, "high": 0, "avg_risk": 0}
    
    total = len(patients_df[patients_df["churn_risk_score"] >= 80])
    critical = len(patients_df[patients_df["churn_risk_score"] >= 90])
    high = total - critical
    avg_risk = patients_df["churn_risk_score"].mean() if "churn_risk_score" in patients_df.columns else 0
    
    return {
        "total_alerts": total,
        "critical": critical,
        "high": high,
        "avg_risk": round(avg_risk, 1)
    }

"""
Trust Labs Report Generation Module
Build and export custom analytics reports.
"""

import pandas as pd
import io
from datetime import datetime


def generate_executive_summary(patients_df, visits_df, branches_df) -> dict:
    """Generate key metrics for executive summary."""
    summary = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_patients": len(patients_df),
        "total_visits": len(visits_df),
        "total_branches": len(branches_df),
    }
    
    if "churn_risk_score" in patients_df.columns:
        summary["high_risk_patients"] = int((patients_df["churn_risk_score"] >= 80).sum())
        summary["avg_risk_score"] = round(patients_df["churn_risk_score"].mean(), 1)
    
    if "patient_tier" in patients_df.columns:
        summary["gold_tier"] = int((patients_df["patient_tier"] == "Gold").sum())
        summary["silver_tier"] = int((patients_df["patient_tier"] == "Silver").sum())
        summary["bronze_tier"] = int((patients_df["patient_tier"] == "Bronze").sum())
    
    if "Gender" in patients_df.columns:
        summary["male_patients"] = int((patients_df["Gender"] == "Male").sum())
        summary["female_patients"] = int((patients_df["Gender"] == "Female").sum())
    
    return summary


def build_report_excel(patients_df, visits_df, branches_df, doctors_df, corporates_df) -> bytes:
    """
    Build a comprehensive Excel report with multiple sheets.
    """
    out = io.BytesIO()
    
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        # Executive Summary
        summary = generate_executive_summary(patients_df, visits_df, branches_df)
        summary_df = pd.DataFrame([summary])
        summary_df.to_excel(writer, sheet_name="Executive Summary", index=False)
        
        # Patients
        if not patients_df.empty:
            patients_df.to_excel(writer, sheet_name="Patients", index=False)
        
        # Visits
        if not visits_df.empty:
            visits_df.to_excel(writer, sheet_name="Visits", index=False)
        
        # Branches
        if not branches_df.empty:
            branches_df.to_excel(writer, sheet_name="Branches", index=False)
        
        # Doctors
        if not doctors_df.empty:
            doctors_df.to_excel(writer, sheet_name="Doctors", index=False)
        
        # Corporate Contracts
        if not corporates_df.empty:
            corporates_df.to_excel(writer, sheet_name="Corporates", index=False)
    
    return out.getvalue()


def build_custom_report(dataframes: dict, sheet_names: dict = None) -> bytes:
    """
    Build a custom Excel report from selected dataframes.
    dataframes: {"sheet_name": df, ...}
    """
    out = io.BytesIO()
    
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        for sheet_name, df in dataframes.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet name max 31 chars
    
    return out.getvalue()


def get_report_history() -> list:
    """Get list of previously generated reports."""
    # In production, this would read from a database or file
    return []


def format_report_filename(report_type: str) -> str:
    """Generate a standardized report filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"trust_labs_{report_type}_{timestamp}.xlsx"

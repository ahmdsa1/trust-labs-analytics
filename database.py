"""
Trust Labs Analytics — Secure Database Layer
Replaces inline SQL with parameterized queries and proper connection management.
"""

import sqlite3
import pandas as pd
import streamlit as st
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_PATH = "trust_labs.db"


@contextmanager
def get_connection():
    """
    Context manager for SQLite connections.
    Ensures connections are properly closed and handles thread safety.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def execute_query(query, params=None):
    """
    Execute a parameterized SQL query and return a DataFrame.
    Safely handles user input via parameter binding.
    """
    try:
        with get_connection() as conn:
            if params:
                return pd.read_sql_query(query, conn, params=params)
            return pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        logger.error(f"Query execution error: {e} | Query: {query} | Params: {params}")
        raise


def search_patient_by_id(patient_id):
    """
    Search for a patient by ID using parameterized query.
    Returns DataFrame or None if not found.
    """
    if not patient_id or not isinstance(patient_id, str):
        return None
    
    query = """
        SELECT * FROM patients 
        WHERE LOWER(Patient_ID) = LOWER(?)
    """
    try:
        result = execute_query(query, [patient_id.strip()])
        return result if not result.empty else None
    except Exception as e:
        logger.error(f"Error searching patient {patient_id}: {e}")
        return None


def search_doctor_by_id(doctor_id):
    """
    Search for a doctor by ID using parameterized query.
    Returns DataFrame or None if not found.
    """
    if not doctor_id or not isinstance(doctor_id, str):
        return None
    
    query = """
        SELECT * FROM doctors 
        WHERE LOWER(Doctor_ID) = LOWER(?)
    """
    try:
        result = execute_query(query, [doctor_id.strip()])
        return result if not result.empty else None
    except sqlite3.Error as e:
        logger.error(f"Error searching doctor {doctor_id}: {e}")
        return None


def search_corporate_by_id(corporate_id):
    """
    Search for a corporate contract by ID using parameterized query.
    Returns DataFrame or None if not found.
    """
    if not corporate_id or not isinstance(corporate_id, str):
        return None
    
    query = """
        SELECT * FROM corporates 
        WHERE LOWER(Corporate_ID) = LOWER(?)
    """
    try:
        result = execute_query(query, [corporate_id.strip()])
        return result if not result.empty else None
    except sqlite3.Error as e:
        logger.error(f"Error searching corporate {corporate_id}: {e}")
        return None


def get_patient_visits(patient_id):
    """
    Get all visits for a patient using parameterized query.
    Returns DataFrame with Visit_Date as datetime.
    """
    if not patient_id or not isinstance(patient_id, str):
        return pd.DataFrame()
    
    query = """
        SELECT Visit_Date, Branch_Name, Visit_Time, Visit_Day
        FROM visits 
        WHERE LOWER(Patient_ID) = LOWER(?)
        ORDER BY Visit_Date DESC
    """
    try:
        df = execute_query(query, [patient_id.strip()])
        df["Visit_Date"] = pd.to_datetime(df["Visit_Date"], errors="coerce")
        return df
    except sqlite3.Error as e:
        logger.error(f"Error getting visits for patient {patient_id}: {e}")
        return pd.DataFrame()


def get_table_data(table_name, limit=None):
    """
    Safely get all data from a table. Validates table name against whitelist.
    """
    ALLOWED_TABLES = {
        "patients", "doctors", "corporates", "branches", 
        "monthly_trends", "monthly_revenue", "revenue_by_test"
    }
    
    if table_name not in ALLOWED_TABLES:
        logger.warning(f"Attempted access to unauthorized table: {table_name}")
        raise ValueError(f"Invalid table name: {table_name}")
    
    query = f"SELECT * FROM {table_name}"
    if limit and isinstance(limit, int) and limit > 0:
        query += f" LIMIT {limit}"
    
    return execute_query(query)


def get_high_risk_patients():
    """
    Get all patients marked as high risk for churn.
    """
    query = """
        SELECT * FROM patients 
        WHERE LOWER(churn_risk_category) = 'high risk'
        ORDER BY churn_risk_score DESC
    """
    try:
        return execute_query(query)
    except sqlite3.Error as e:
        logger.error(f"Error fetching high-risk patients: {e}")
        return pd.DataFrame()


def load_patients():
    """Load all patients with caching."""
    return execute_query("SELECT * FROM patients")


def load_visits():
    """Load all visits and parse dates."""
    df = execute_query("SELECT * FROM visits")
    df["Visit_Date"] = pd.to_datetime(df["Visit_Date"], errors="coerce")
    # Visit_Month is stored as text month name (e.g. "August");
    # combine with year from Visit_Date to create proper datetime
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df["_month_num"] = df["Visit_Month"].map(month_map)
    default_year = int(df["Visit_Date"].dt.year.mode()[0]) if not df["Visit_Date"].empty else 2024
    df["_year"] = df["Visit_Date"].dt.year.fillna(default_year).astype(int)
    df["Visit_Month"] = pd.to_datetime(
        df["_year"].astype(str) + "-" + df["_month_num"].astype(str) + "-1",
        errors="coerce"
    )
    df = df.drop(columns=["_month_num", "_year"])
    return df



def load_doctors():
    """Load doctors data with fallback."""
    try:
        return execute_query("SELECT * FROM doctors")
    except sqlite3.Error:
        return pd.DataFrame({"doctor_id": [], "actual_referrals": []})


def load_corporates():
    """Load corporates data with fallback."""
    try:
        return execute_query("SELECT * FROM corporates")
    except sqlite3.Error:
        return pd.DataFrame({"corporate_id": [], "actual_visits": []})


def load_branches():
    """Load branches data."""
    return execute_query("SELECT * FROM branches")


def load_monthly_trends():
    """Load monthly trends with date parsing."""
    try:
        df = execute_query("SELECT * FROM monthly_trends")
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except sqlite3.Error:
        return pd.DataFrame()


def load_monthly_revenue():
    """Load monthly revenue with date parsing."""
    try:
        df = execute_query("SELECT * FROM monthly_revenue")
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except sqlite3.Error:
        return pd.DataFrame()


def load_revenue_by_test(limit=20):
    """Load top revenue-generating tests."""
    query = "SELECT * FROM revenue_by_test ORDER BY total_revenue DESC LIMIT ?"
    return execute_query(query, [limit])

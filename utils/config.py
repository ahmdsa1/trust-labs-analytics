"""
Trust Labs Data Pipeline - Configuration
"""

import os

# ============================================
# GOOGLE SHEETS SETTINGS
# ============================================

SPREADSHEET_NAME = "Trust Labs - Patient Database"
PATIENTS_SHEET = "Patients"
VISITS_SHEET = "Visits"

# ============================================
# FOLDER PATHS
# ============================================

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(PROJECT_FOLDER, "data")
OUTPUT_FOLDER = os.path.join(PROJECT_FOLDER, "output")
LOGS_FOLDER = os.path.join(PROJECT_FOLDER, "logs")
CREDENTIALS_FILE = os.path.join(PROJECT_FOLDER, "credentials.json")

# ============================================
# COLUMN MAPPINGS (ACTUAL CSV COLUMNS)
# ============================================

# These match your actual CSV files
CSV_COLUMNS = [
    'Visit_Date', 'Visit_Number', 'Visit_Day', 'Visit_Month', 
    'Branch_ID', 'Branch_Name', 'Branch_City', 
    'Patient_ID', 'Age_Group', 'Gender', 'Patient_Type',
    'Has_Diabetes', 'Has_Hypertension', 'Distance_Category',
    'Total_Visits_Expected', 'Retention_Category',
    'Visit_Hour', 'Visit_Time', 'Is_Fasting_Time',
    'Is_Weekend', 'Is_Peak_Hour', 'Is_Return_Visit'
]

# Patient columns to extract
PATIENT_COLUMNS = [
    'Patient_ID', 'Age_Group', 'Gender', 'Patient_Type',
    'Has_Diabetes', 'Has_Hypertension', 'Distance_Category',
    'Total_Visits_Expected', 'Retention_Category'
]

# Visit columns
VISIT_COLUMNS = [
    'Visit_Date', 'Visit_Number', 'Visit_Day', 'Visit_Month',
    'Patient_ID', 'Branch_ID', 'Branch_Name', 'Branch_City',
    'Visit_Hour', 'Visit_Time', 'Is_Fasting_Time',
    'Is_Weekend', 'Is_Peak_Hour', 'Is_Return_Visit'
]

# ============================================
# DEDUPLICATION
# ============================================

PATIENT_UNIQUE_KEY = 'Patient_ID'
VISIT_UNIQUE_KEYS = ['Patient_ID', 'Visit_Date', 'Visit_Number']

# ============================================
# LOGGING
# ============================================

LOG_FILE = os.path.join(LOGS_FOLDER, 'pipeline.log')
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# ============================================
# UPLOAD SETTINGS
# ============================================

UPLOAD_BATCH_SIZE = 500
API_DELAY = 1.0

print("✅ Config loaded!")
import sqlite3
import pandas as pd

conn = sqlite3.connect('trust_labs.db', check_same_thread=False)

# Test load_visits equivalent
df = pd.read_sql("SELECT * FROM visits", conn)
print("Visits columns before rename:", list(df.columns))
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
})
print("Visits columns after rename:", list(df.columns))
print("Amount_Paid in columns:", "Amount_Paid" in df.columns)
print("patient_tier in columns:", "patient_tier" in df.columns)
print("Amount_Paid sample:", df["Amount_Paid"].head().tolist() if "Amount_Paid" in df.columns else "N/A")
print("patient_tier sample:", df["patient_tier"].head().tolist() if "patient_tier" in df.columns else "N/A")
print()

# Test load_doctors equivalent
df2 = pd.read_sql("SELECT * FROM doctors", conn)
print("Doctors columns before rename:", list(df2.columns))
df2 = df2.rename(columns={"specialty_en": "specialty"})
print("Doctors columns after rename:", list(df2.columns))
print("branch_id in columns:", "branch_id" in df2.columns)
print("specialty in columns:", "specialty" in df2.columns)
print()

# Test doctor_branch
df3 = pd.read_sql("SELECT * FROM doctor_branch", conn)
print("Doctor branch columns:", list(df3.columns))
print("Doctor branch sample:", df3.head().to_string())
print()

# Test filtered visits with date filter
df["Visit_Date"] = pd.to_datetime(df["Visit_Date"], errors="coerce")
print("Visit_Date min:", df["Visit_Date"].min())
print("Visit_Date max:", df["Visit_Date"].max())
print("Visit_Date nulls:", df["Visit_Date"].isna().sum())

date_start = df["Visit_Date"].min()
date_end = df["Visit_Date"].max()
filtered = df[(df["Visit_Date"] >= date_start) & (df["Visit_Date"] <= date_end)]
print("Filtered visits shape:", filtered.shape)
print("Amount_Paid in filtered:", "Amount_Paid" in filtered.columns)
print("Branch_Name in filtered:", "Branch_Name" in filtered.columns)

conn.close()

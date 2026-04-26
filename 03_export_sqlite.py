"""
=============================================================================
FOHOSAT LABS — STEP 3: EXPORT TO SQLITE
=============================================================================
Reads all analysis-ready CSVs from output/powerbi_tables/ and writes them
to a single trust_labs.db SQLite database with proper indexes.
=============================================================================
"""

import sqlite3
import pandas as pd
import os

print("=" * 75)
print("FOHOSAT LABS — SQLITE EXPORT")
print("=" * 75)

PBI_DIR = "output/powerbi_tables"
DB_PATH = "trust_labs.db"

# ─────────────────────────────────────────────────────────────────────────────
# LOAD CSVs
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/4] Loading CSVs...")

TABLES = {
    # name in DB          : CSV filename (relative to PBI_DIR)
    "patients":            "patients.csv",
    "visits":              "visits.csv",
    "doctors":             "doctors.csv",
    "corporates":          "corporates.csv",
    "branches":            "branches.csv",
    "monthly_trends":      "monthly_trends.csv",
    "monthly_revenue":     "monthly_revenue.csv",
    "churn_segments":      "churn_segments.csv",
    "demographics":        "demographics.csv",
    "revenue_by_test":     "revenue_by_test.csv",
    "hourly_patterns":     "hourly_patterns.csv",
    "dow_patterns":        "dow_patterns.csv",
    "daily_stats":         "daily_stats.csv",
    "branch_comparison":   "branch_comparison.csv",  # dedicated comparison table
    "doctor_branch":       "doctor_branch.csv",
    "tat_by_test":         "tat_by_test.csv",
    "tat_by_branch":       "tat_by_branch.csv",
    "home_collection":     "home_collection.csv",
    "home_collection_trend":"home_collection_trend.csv",
    "cohort_retention":    "cohort_retention.csv",
    "test_associations":   "test_associations.csv",
}

loaded = {}
for table_name, csv_file in TABLES.items():
    path = os.path.join(PBI_DIR, csv_file)
    if os.path.exists(path):
        df = pd.read_csv(path, low_memory=False)
        loaded[table_name] = df
        print(f"  ✓ {table_name:<30} {len(df):>8,} rows")
    else:
        print(f"  ⚠  {table_name:<30} MISSING: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# DATE FORMATTING — ensure all date columns are ISO strings
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/4] Normalising date columns...")

DATE_COLS = {
    "patients":   ["first_visit_date","last_visit_date"],
    "visits":     ["visit_date","visit_month"],
    "doctors":    ["first_referral_date","first_referral","last_referral"],
    "corporates": ["contract_start","contract_end","first_visit","last_visit"],
    "monthly_trends":  ["visit_month"],
    "monthly_revenue": ["visit_month"],
    "daily_stats":     ["visit_date"],
    "home_collection_trend": ["request_date"],
}

for table, cols in DATE_COLS.items():
    if table not in loaded:
        continue
    for col in cols:
        if col in loaded[table].columns:
            loaded[table][col] = pd.to_datetime(
                loaded[table][col], errors="coerce"
            ).dt.strftime("%Y-%m-%d")

print("  ✓ Date columns normalised")

# ─────────────────────────────────────────────────────────────────────────────
# WRITE TO SQLITE
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n[3/4] Writing to {DB_PATH}...")

# Remove old DB so we start clean
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

con = sqlite3.connect(DB_PATH)

for table_name, df in loaded.items():
    df.to_sql(table_name, con, if_exists="replace", index=False)
    print(f"  ✓ {table_name}")

# ─────────────────────────────────────────────────────────────────────────────
# INDEXES — for fast Streamlit queries
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/4] Creating indexes...")

INDEXES = [
    # patients
    ("idx_pat_id",        "patients",          "patient_id"),
    ("idx_pat_churn",     "patients",          "churn_risk_category"),
    ("idx_pat_tier",      "patients",          "patient_tier"),
    ("idx_pat_type",      "patients",          "patient_type"),
    ("idx_pat_branch",    "patients",          "primary_branch_id"),
    # visits
    ("idx_vis_patient",   "visits",            "patient_id"),
    ("idx_vis_date",      "visits",            "visit_date"),
    ("idx_vis_branch",    "visits",            "branch_id"),
    ("idx_vis_month",     "visits",            "visit_month"),
    ("idx_vis_source",    "visits",            "visit_source"),
    ("idx_vis_hour",      "visits",            "visit_hour"),
    ("idx_vis_doctor",    "visits",            "referring_doctor_id"),
    ("idx_vis_corp",      "visits",            "corporate_id"),
    # doctors
    ("idx_doc_id",        "doctors",           "doctor_id"),
    ("idx_doc_spec",      "doctors",           "specialty_en"),
    ("idx_doc_status",    "doctors",           "doctor_status"),
    # corporates
    ("idx_corp_id",       "corporates",        "corporate_id"),
    ("idx_corp_health",   "corporates",        "contract_health"),
    # operational tables
    ("idx_hp_branch",     "hourly_patterns",   "branch_name_ar"),
    ("idx_hp_hour",       "hourly_patterns",   "visit_hour"),
    ("idx_dow_branch",    "dow_patterns",      "branch_name_ar"),
    ("idx_ds_date",       "daily_stats",       "visit_date"),
    ("idx_ds_branch",     "daily_stats",       "branch_name_ar"),
    ("idx_db_doctor",     "doctor_branch",     "doctor_id"),
    ("idx_db_branch",     "doctor_branch",     "branch_id"),
    ("idx_tat_test",      "tat_by_test",       "test_name"),
    ("idx_tat_br",        "tat_by_branch",     "branch_id"),
    ("idx_hc_zone",       "home_collection",   "zone_name"),
    ("idx_cohort_month",  "cohort_retention",  "cohort_month"),
    ("idx_doc_branch",    "doctors",           "branch_id"),
    ("idx_vis_tier",      "visits",            "patient_tier"),
    ("idx_vis_amount",    "visits",            "amount_paid"),
    ("idx_bc_branch",     "branch_comparison", "branch_id"),
    ("idx_bc_city",       "branch_comparison", "city_ar"),
]

for idx_name, table, column in INDEXES:
    try:
        con.execute(
            f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})")
    except Exception as e:
        print(f"  ⚠  Could not create {idx_name}: {e}")

con.commit()
print(f"  ✓ {len(INDEXES)} indexes created")

# ─────────────────────────────────────────────────────────────────────────────
# VERIFY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*75)
print("VERIFICATION")
print("="*75)

all_tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con)
print(f"\n  Tables in database: {len(all_tables)}\n")
for t in all_tables["name"]:
    cnt = pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", con)["n"][0]
    print(f"  ✓ {t:<35} {cnt:>8,} rows")

con.close()

db_mb = os.path.getsize(DB_PATH) / 1024 / 1024
print(f"\n  Database size: {db_mb:.1f} MB")
print(f"  Location:      {os.path.abspath(DB_PATH)}")
print("\n  ✅ SQLite database ready — launch Streamlit with:")
print("     streamlit run app.py")
print("="*75)

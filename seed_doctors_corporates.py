#!/usr/bin/env python3
"""
Generate realistic synthetic doctors and corporates data
from existing patients/visits and seed into trust_labs.db.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

conn = sqlite3.connect("trust_labs.db")

# ── Load existing data ──
patients = pd.read_sql("SELECT * FROM patients", conn)
visits   = pd.read_sql("SELECT * FROM visits", conn)
branches = pd.read_sql("SELECT * FROM branches", conn)

print(f"Patients: {len(patients):,} | Visits: {len(visits):,} | Branches: {len(branches)}")

# ============================================================
# GENERATE DOCTORS
# ============================================================

SPECIALTIES = [
    "Internal Medicine", "Cardiology", "Endocrinology", "General Practice",
    "Family Medicine", "Nephrology", "Gastroenterology", "Pulmonology",
    "Rheumatology", "Hematology", "Infectious Disease", "Neurology",
    "Dermatology", "Ophthalmology", "ENT", "Orthopedics", "Urology",
    "Obstetrics & Gynecology", "Pediatrics", "Oncology"
]

N_DOCTORS = 60

doctor_ids = [f"DOC{str(i).zfill(5)}" for i in range(1, N_DOCTORS + 1)]
doctor_names = [f"Dr. {np.random.choice(['Ahmed', 'Mohamed', 'Ali', 'Hassan', 'Omar', 'Khaled', 'Tarek', 'Mahmoud', 'Ibrahim', 'Youssef', 'Samer', 'Wael', 'Hossam', 'Amr', 'Bassem', 'Karim', 'Nabil', 'Sherif', 'Essam', 'Adel'])} {np.random.choice(['El-Sayed', 'Hassan', 'Ibrahim', 'Mohamed', 'Ali', 'Omar', 'Mahmoud', 'Khalil', 'Fouad', 'Rashid', 'Nour', 'Fathi', 'Ghaly', 'Salem', 'Darwish'])}" for _ in range(N_DOCTORS)]

# Distribute referral counts (power law — few doctors get many referrals)
referral_counts = np.random.pareto(1.5, N_DOCTORS) * 50
referral_counts = np.clip(referral_counts, 5, 800).astype(int)

# Unique patients referred (correlated with referrals)
unique_patients = (referral_counts * np.random.uniform(0.6, 0.95, N_DOCTORS)).astype(int)
unique_patients = np.clip(unique_patients, 3, referral_counts)

# Revenue generated (avg 150-300 EGP per referral)
avg_per_ref = np.random.uniform(120, 350, N_DOCTORS)
total_revenue = (referral_counts * avg_per_ref).astype(int)

# Performance category
performance = []
for refs in referral_counts:
    if refs >= 400:
        performance.append("Exceeds Expectations")
    elif refs >= 200:
        performance.append("Meets Expectations")
    elif refs >= 100:
        performance.append("Average")
    elif refs >= 50:
        performance.append("Below Average")
    else:
        performance.append("Needs Improvement")

# Top referring branch (randomly assign)
top_branch = np.random.choice(branches["Branch_Name"].tolist(), N_DOCTORS)

# Years of experience
years_exp = np.random.randint(1, 30, N_DOCTORS)

# Commission rate
commission_rate = np.round(np.random.uniform(0.05, 0.15, N_DOCTORS), 3)

# Active status (90% active)
is_active = np.random.choice([1, 0], N_DOCTORS, p=[0.9, 0.1])

# Last referral date (within last 90 days for active doctors)
last_ref_dates = []
for active in is_active:
    if active:
        days_ago = np.random.randint(1, 90)
    else:
        days_ago = np.random.randint(91, 365)
    date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime("%Y-%m-%d")
    last_ref_dates.append(date)

# Trend (MoM change)
trend = np.round(np.random.uniform(-15, 25, N_DOCTORS), 1)

doctors_df = pd.DataFrame({
    "doctor_id": doctor_ids,
    "doctor_name": doctor_names,
    "specialty": np.random.choice(SPECIALTIES, N_DOCTORS),
    "actual_referrals": referral_counts,
    "unique_patients_referred": unique_patients,
    "total_revenue_generated": total_revenue,
    "performance_category": performance,
    "top_referring_branch": top_branch,
    "years_experience": years_exp,
    "commission_rate": commission_rate,
    "is_active": is_active,
    "last_referral_date": last_ref_dates,
    "referral_trend_pct": trend
})

# Sort by referrals descending
doctors_df = doctors_df.sort_values("actual_referrals", ascending=False).reset_index(drop=True)

print(f"\nGenerated {len(doctors_df)} doctors")
print(doctors_df.head(3).to_string())

# ============================================================
# GENERATE CORPORATES
# ============================================================

COMPANY_NAMES = [
    "Egyptian Petrochemicals Co.", "Cairo Steel Industries", "Nile Pharma Group",
    "Alexandria Shipping Corp", "Suez Canal Authority", "EgyptAir Maintenance",
    "Delta Sugar Company", "Eastern Tobacco", "Orascom Construction",
    "Qalaa Holdings", "Talaat Moustafa Group", "Palm Hills Developments",
    "EFG Hermes", "Commercial International Bank", "QNB Al Ahli",
    "Misr Insurance", "Arab Contractors", "Hassan Allam Holdings",
    "El Sewedy Electric", "Ezz Steel", "Sodic", "Madinet Nasr Housing",
    "Juhayna Food Industries", "Edita Food Industries", "Obour Land",
    "Dice Sports & Casual Wear", " Pharos Holding", "Beltone Financial",
    "Fawry Banking", "SwipeCX", "Wuzzuf", "Vezeeta", "Breadfast",
    "MaxAB", "Capiter", "Rabbit", "Telda", "MoneyFellows", "Halan"
]

INDUSTRIES = [
    "Oil & Gas", "Manufacturing", "Pharmaceuticals", "Logistics",
    "Government", "Aviation", "Food & Beverage", "Tobacco",
    "Construction", "Investment", "Real Estate", "Real Estate",
    "Investment Banking", "Banking", "Banking",
    "Insurance", "Construction", "Engineering",
    "Electrical", "Steel", "Real Estate", "Real Estate",
    "FMCG", "FMCG", "FMCG",
    "Retail", "Investment", "Financial Services",
    "Fintech", "SaaS", "HR Tech", "Health Tech", "E-commerce",
    "B2B Commerce", "B2B Commerce", "Delivery", "Fintech", "Fintech", "Mobility"
]

N_CORPS = min(len(COMPANY_NAMES), 35)

# Employee counts (log-normal distribution)
employee_counts = np.random.lognormal(5, 1.2, N_CORPS).astype(int)
employee_counts = np.clip(employee_counts, 50, 5000)

# Contract types
contract_types = np.random.choice(
    ["Premium", "Standard", "Basic", "Enterprise"],
    N_CORPS,
    p=[0.15, 0.45, 0.25, 0.15]
)

# Unique employees who visited (30-80% of total)
unique_employees = (employee_counts * np.random.uniform(0.25, 0.75, N_CORPS)).astype(int)

# Utilization rate
utilization = np.round(unique_employees / employee_counts, 3)

# Actual visits generated (avg 2-5 visits per active employee)
visits_per_emp = np.random.uniform(1.5, 6.0, N_CORPS)
actual_visits = (unique_employees * visits_per_emp).astype(int)

# Revenue (avg 200-500 EGP per visit)
revenue_per_visit = np.random.uniform(180, 450, N_CORPS)
total_revenue = (actual_visits * revenue_per_visit).astype(int)

# Contract health
health = []
for u, rev in zip(utilization, total_revenue):
    if u >= 0.6 and rev > 500000:
        health.append("Excellent")
    elif u >= 0.45:
        health.append("Good")
    elif u >= 0.3:
        health.append("Fair")
    else:
        health.append("At Risk")

# Contract start date
start_dates = []
for _ in range(N_CORPS):
    months_ago = np.random.randint(3, 36)
    date = (datetime.now() - pd.Timedelta(days=months_ago*30)).strftime("%Y-%m-%d")
    start_dates.append(date)

# Discount rate
discount = np.round(np.random.uniform(0.05, 0.25, N_CORPS), 2)

# Renewals
renewals = np.random.randint(0, 4, N_CORPS)

# Satisfaction score
satisfaction = np.round(np.random.uniform(6.5, 9.8, N_CORPS), 1)

# Trend
contract_trend = np.round(np.random.uniform(-10, 20, N_CORPS), 1)

corps_df = pd.DataFrame({
    "corporate_id": [f"CORP{str(i).zfill(3)}" for i in range(1, N_CORPS + 1)],
    "company_name": COMPANY_NAMES[:N_CORPS],
    "industry": INDUSTRIES[:N_CORPS],
    "employee_count": employee_counts,
    "contract_type": contract_types,
    "unique_employees": unique_employees,
    "actual_utilization_rate": utilization,
    "actual_visits": actual_visits,
    "total_revenue": total_revenue,
    "contract_health": health,
    "contract_start_date": start_dates,
    "discount_rate": discount,
    "renewals_count": renewals,
    "satisfaction_score": satisfaction,
    "visit_trend_pct": contract_trend
})

# Sort by revenue descending
corps_df = corps_df.sort_values("total_revenue", ascending=False).reset_index(drop=True)

print(f"\nGenerated {len(corps_df)} corporate contracts")
print(corps_df.head(3).to_string())

# ============================================================
# SAVE TO DATABASE
# ============================================================

doctors_df.to_sql("doctors", conn, if_exists="replace", index=False)
corps_df.to_sql("corporates", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print(f"\n✅ Seeded database with {len(doctors_df)} doctors and {len(corps_df)} corporates")


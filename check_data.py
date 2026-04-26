import sqlite3
import pandas as pd
conn = sqlite3.connect('trust_labs.db')

# Check amount_paid in visits
df = pd.read_sql('SELECT amount_paid, patient_tier FROM visits LIMIT 5', conn)
print('=== Visits sample ===')
print(df)
print('amount_paid nulls:', df['amount_paid'].isna().sum())
print('amount_paid zeros:', (df['amount_paid'] == 0).sum())
print('amount_paid mean:', df['amount_paid'].mean())

# Check patient_tier in patients
df2 = pd.read_sql('SELECT patient_tier FROM patients LIMIT 5', conn)
print()
print('=== Patients sample ===')
print(df2)
print('patient_tier value counts:')
print(pd.read_sql('SELECT patient_tier, COUNT(*) as cnt FROM patients GROUP BY patient_tier', conn))

# Check doctors branch_id
df3 = pd.read_sql('SELECT doctor_id, branch_id, specialty_en FROM doctors LIMIT 5', conn)
print()
print('=== Doctors sample ===')
print(df3)
print('branch_id nulls:', df3['branch_id'].isna().sum())

# Check visits amount_paid distribution
print()
print('=== amount_paid stats ===')
print(pd.read_sql('SELECT MIN(amount_paid) as min, MAX(amount_paid) as max, AVG(amount_paid) as avg FROM visits', conn))

conn.close()

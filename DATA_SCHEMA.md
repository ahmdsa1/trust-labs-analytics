# Data Schema & Requirements

## Database Tables

### Patients Table
```sql
CREATE TABLE patients (
    Patient_ID TEXT PRIMARY KEY,
    Age_Group TEXT,
    Gender TEXT,
    Patient_Type TEXT,
    Has_Diabetes INTEGER,
    Has_Hypertension INTEGER,
    Distance_Category TEXT,
    Total_Visits_Expected INTEGER,
    Retention_Category TEXT,
    churn_risk_score REAL,
    churn_risk_category TEXT,
    patient_tier TEXT,
    loyalty_points INTEGER,
    last_visit_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Columns:**
- `Patient_ID` (TEXT): Unique patient identifier
- `Age_Group` (TEXT): Age bracket (e.g., "25-35", "35-45")
- `Gender` (TEXT): "Male" or "Female"
- `Patient_Type` (TEXT): "Regular", "Corporate", "Occasional"
- `Has_Diabetes` (INTEGER): 0 = No, 1 = Yes
- `Has_Hypertension` (INTEGER): 0 = No, 1 = Yes
- `Distance_Category` (TEXT): "Near", "Medium", "Far"
- `Total_Visits_Expected` (INTEGER): Expected annual visits
- `Retention_Category` (TEXT): "High", "Medium", "Low"
- `churn_risk_score` (REAL): 0-100 risk score
- `churn_risk_category` (TEXT): "Low Risk", "Medium Risk", "High Risk"
- `patient_tier` (TEXT): "Gold", "Silver", "Bronze"
- `loyalty_points` (INTEGER): Accumulated rewards points
- `last_visit_date` (DATE): Most recent visit
- `created_at`, `updated_at` (TIMESTAMP): Record timestamps

---

### Visits Table
```sql
CREATE TABLE visits (
    Visit_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Patient_ID TEXT NOT NULL,
    Visit_Date DATE NOT NULL,
    Visit_Number INTEGER,
    Visit_Day TEXT,
    Visit_Month TEXT,
    Branch_ID TEXT,
    Branch_Name TEXT,
    Branch_City TEXT,
    Visit_Hour INTEGER,
    Visit_Time TEXT,
    Is_Fasting_Time INTEGER,
    Is_Weekend INTEGER,
    Is_Peak_Hour INTEGER,
    Is_Return_Visit INTEGER,
    Visit_Duration INTEGER,
    Services_Rendered TEXT,
    Amount_Paid REAL,
    created_at TIMESTAMP,
    FOREIGN KEY(Patient_ID) REFERENCES patients(Patient_ID)
);
```

**Columns:**
- `Visit_ID` (INTEGER): Unique visit identifier
- `Patient_ID` (TEXT): Reference to patient
- `Visit_Date` (DATE): Date of visit (format: YYYY-MM-DD)
- `Visit_Number` (INTEGER): Sequential visit number for this patient
- `Visit_Day` (TEXT): Day of week (Monday, Tuesday, etc.)
- `Visit_Month` (TEXT): Month name (January, February, etc.)
- `Branch_ID`, `Branch_Name`, `Branch_City` (TEXT): Branch information
- `Visit_Hour` (INTEGER): Hour of visit (0-23)
- `Visit_Time` (TEXT): Time period (Morning, Afternoon, Evening, Night)
- `Is_Fasting_Time` (INTEGER): 0 = No, 1 = Yes (for fasting tests)
- `Is_Weekend` (INTEGER): 0 = Weekday, 1 = Weekend
- `Is_Peak_Hour` (INTEGER): 0 = Off-peak, 1 = Peak hours
- `Is_Return_Visit` (INTEGER): 0 = First visit, 1 = Return visit
- `Visit_Duration` (INTEGER): Duration in minutes
- `Services_Rendered` (TEXT): Types of tests/services
- `Amount_Paid` (REAL): Payment amount
- `created_at` (TIMESTAMP): Record creation timestamp

---

### Branches Table
```sql
CREATE TABLE branches (
    Branch_ID TEXT PRIMARY KEY,
    Branch_Name TEXT,
    Branch_City TEXT,
    Address TEXT,
    Phone TEXT,
    Manager_Name TEXT,
    Total_Visits INTEGER,
    Total_Patients INTEGER,
    Performance_Score REAL,
    Revenue_Mtd REAL,
    Capacity_Utilization REAL,
    Created_At TIMESTAMP
);
```

**Columns:**
- `Branch_ID` (TEXT): Unique branch identifier
- `Branch_Name` (TEXT): Branch name (e.g., "Mohandessin HQ")
- `Branch_City` (TEXT): City location (Cairo, Alexandria, etc.)
- `Address` (TEXT): Full address
- `Phone` (TEXT): Contact number
- `Manager_Name` (TEXT): Branch manager
- `Total_Visits` (INTEGER): Cumulative visits
- `Total_Patients` (INTEGER): Unique patients served
- `Performance_Score` (REAL): 0-100 rating
- `Revenue_Mtd` (REAL): Month-to-date revenue
- `Capacity_Utilization` (REAL): Percentage (0-100)
- `Created_At` (TIMESTAMP): Record timestamp

---

## CSV File Requirements

If importing from CSV instead of database:

### patients.csv
```
Patient_ID,Age_Group,Gender,Patient_Type,Has_Diabetes,Has_Hypertension,Distance_Category,Total_Visits_Expected,Retention_Category
P001,25-35,Male,Regular,0,0,Near,12,High
P002,35-45,Female,Corporate,1,0,Medium,24,High
```

### visits.csv
```
Visit_Date,Visit_Number,Visit_Day,Visit_Month,Patient_ID,Branch_ID,Branch_Name,Branch_City,Visit_Hour,Visit_Time,Is_Fasting_Time,Is_Weekend,Is_Peak_Hour,Is_Return_Visit
2024-01-15,1,Monday,January,P001,B01,Mohandessin HQ,Cairo,08,Morning,1,0,1,0
2024-01-16,2,Tuesday,January,P002,B02,Dokki,Cairo,10,Morning,0,0,0,1
```

### branches.csv
```
Branch_ID,Branch_Name,Branch_City,Address,Phone,Manager_Name,Total_Visits,Total_Patients,Performance_Score,Revenue_Mtd,Capacity_Utilization
B01,Mohandessin HQ,Cairo,12 Ahmed Pasha St,01010000000,Ahmed Hassan,5000,800,92.5,450000,85
B02,Dokki,Cairo,45 Nile St,01010000001,Fatma Mohamed,3800,650,88.3,320000,78
```

---

## Data Validation Rules

1. **Date Format**: All dates must be YYYY-MM-DD
2. **Patient_ID**: Must be unique and non-empty
3. **Numeric Fields**: Age, visits, scores should be integers or floats
4. **Categorical**: Gender (Male/Female), Days (Monday-Sunday), Months (January-December)
5. **Risk Scores**: Must be between 0-100
6. **Facility Scores**: Must be between 0-100

---

## Notes for Data Import

- Ensure no duplicate Patient_IDs in patients table
- All visits must reference valid Patient_IDs
- Dates must be in correct format; invalid dates will be skipped
- Empty cells should be NULL or 0 depending on column type
- Consider indexing frequently queried columns (Patient_ID, Branch_ID, Visit_Date)

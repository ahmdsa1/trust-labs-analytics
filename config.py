"""
Trust Labs Analytics — Centralized Configuration
Moves all hardcoded business values and settings to a single source of truth.
"""

# ============================================================
# INFLATION SETTINGS
# ============================================================

# Annual inflation rate (as decimal). Egypt's current rate.
# Update this value quarterly based on official statistics.
ANNUAL_INFLATION_RATE = 0.33

# ============================================================
# REVENUE ASSUMPTIONS
# ============================================================

# Average revenue per visit in EGP
# Should be updated based on actual historical averages
AVG_REVENUE_PER_VISIT = 150

# Profit margin (as decimal)
PROFIT_MARGIN = 0.65

# ============================================================
# RISK SCORING THRESHOLDS
# ============================================================

RISK_THRESHOLDS = {
    "low": 30,
    "medium": 60,
    "high": 100
}

RISK_LABELS = {
    "low": "Low",
    "medium": "Medium", 
    "high": "High"
}

# ============================================================
# PATIENT TIERS
# ============================================================

TIERS = ["Gold", "Silver", "Bronze"]

# ============================================================
# SEARCH VALIDATION
# ============================================================

MAX_ID_LENGTH = 50
ALLOWED_ID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")

# ============================================================
# FORECASTING
# ============================================================

DEFAULT_FORECAST_MONTHS = 3
FORECAST_CONFIDENCE_LEVEL = 1.0  # Standard deviations for confidence band

# ============================================================
# PERFORMANCE CATEGORIES
# ============================================================

PERFORMANCE_EXCEEDS = "Exceeds Expectations"
PERFORMANCE_GOOD = "Good"
PERFORMANCE_AVERAGE = "Average"
PERFORMANCE_BELOW = "Below Expectations"

# ============================================================
# EXPORT SETTINGS
# ============================================================

EXPORT_TABLES = {
    "Patients": "patients",
    "Doctors": "doctors", 
    "Corporate Contracts": "corporates",
    "Branches": "branches",
    "High Risk Patients": "high_risk"
}

# ============================================================
# COLOR PALETTE (Google Material)
# ============================================================

COLORS = {
    "primary": "#1a73e8",
    "success": "#34a853",
    "warning": "#fbbc04",
    "danger": "#ea4335",
    "purple": "#9334e6",
    "gray": "#9aa0a6",
    "bronze": "#cd7f32",
}

# ============================================================
# AUTHENTICATION
# ============================================================

SESSION_TIMEOUT_MINUTES = 60
AUTH_ENABLED = True  # Set to False to disable authentication

# ============================================================
# ALERTS
# ============================================================

ALERT_RISK_THRESHOLD = 80
ALERT_CRITICAL_THRESHOLD = 90
MAX_ALERTS_DISPLAY = 10

# ============================================================
# REAL-TIME REFRESH
# ============================================================

AUTO_REFRESH_SECONDS = 300  # 5 minutes
ENABLE_AUTO_REFRESH = False  # Set to True for production

# ============================================================
# MOBILE RESPONSIVE
# ============================================================

MOBILE_BREAKPOINT = 768  # px

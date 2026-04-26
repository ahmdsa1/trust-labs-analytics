#!/usr/bin/env python3
"""
Safely remove emojis from app.py using targeted replacements
"""

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_emojis(content):
    # Sidebar navigation - remove emojis from page names
    content = content.replace('"🏠  Home"', '"Home"')
    content = content.replace('"🔍  Patient Search"', '"Patient Search"')
    content = content.replace('"👨‍⚕️  Doctor Search"', '"Doctor Search"')
    content = content.replace('"🏢  Corporate Search"', '"Corporate Search"')
    content = content.replace('"👨‍⚕️  Doctors"', '"Doctors"')
    content = content.replace('"📊  Analytics"', '"Analytics"')
    content = content.replace('"📥  Export"', '"Export"')
    content = content.replace('"📋 Reports"', '"Reports"')

    # Sidebar header
    content = content.replace('<span style="font-size:1.6rem">🏥</span>', '<span style="font-size:1.6rem"></span>')

    # Page headers
    content = content.replace('<h1>Analytics Dashboard</h1>', '<h1>Analytics Dashboard</h1>')
    content = content.replace('<h1>Patient Search</h1>', '<h1>Patient Search</h1>')
    content = content.replace('<h1>Doctor Performance</h1>', '<h1>Doctor Performance</h1>')
    content = content.replace('<h1>Corporate Contracts</h1>', '<h1>Corporate Contracts</h1>')
    content = content.replace('<h1>Doctor Ranking Dashboard</h1>', '<h1>Doctor Ranking Dashboard</h1>')
    content = content.replace('<h1>Export Data</h1>', '<h1>Export Data</h1>')
    content = content.replace('<h1>Reports & Exports</h1>', '<h1>Reports & Exports</h1>')

    # Tab labels
    content = content.replace('["📊 Overview", "⚠️ Churn", "💰 Revenue & Inflation (CAGR)", "🔮 Predictive Trends", "🏥 Clinical Insights", "🔍 Data Quality", "🏥 Branch Ops", "💎 Revenue Mix", "⚔️ Branch Compare"]',
                              '["Overview", "Churn", "Revenue & Inflation (CAGR)", "Predictive Trends", "Clinical Insights", "Data Quality", "Branch Ops", "Revenue Mix", "Branch Compare"]')

    content = content.replace('["🏆 Ranking", "⚠️ At-Risk Alerts", "🏥 Branch Flow"]',
                              '["Ranking", "At-Risk Alerts", "Branch Flow"]')

    content = content.replace('["🔍 Contract Search", "📊 Utilization Gap"]',
                              '["Contract Search", "Utilization Gap"]')

    content = content.replace('["🆔 ID Lookup", "🔎 Advanced Search"]',
                              '["ID Lookup", "Advanced Search"]')

    content = content.replace('["📊 Full Report", "🛠️ Custom Report"]',
                              '["Full Report", "Custom Report"]')

    # Section titles - remove emojis
    content = content.replace('sec_title("👥 Gender Distribution")', 'sec_title("Gender Distribution")')
    content = content.replace('sec_title("⚠️ Churn Risk Levels")', 'sec_title("Churn Risk Levels")')
    content = content.replace('sec_title("📈 Monthly Visit Trends")', 'sec_title("Monthly Visit Trends")')
    content = content.replace('sec_title("🏆 Patient Tiers")', 'sec_title("Patient Tiers")')
    content = content.replace('sec_title("🏥 Top 5 Branches")', 'sec_title("Top 5 Branches")')
    content = content.replace('sec_title("👥 Age Distribution")', 'sec_title("Age Distribution")')
    content = content.replace('sec_title("🕐 Visit Heatmap — Day × Hour"', 'sec_title("Visit Heatmap — Day x Hour"')
    content = content.replace('sec_title("📊 Month-over-Month Growth"', 'sec_title("Month-over-Month Growth"')
    content = content.replace('sec_title("💸 No-Show Cost Estimator")', 'sec_title("No-Show Cost Estimator")')
    content = content.replace('sec_title("🔴 High Risk"', 'sec_title("High Risk"')
    content = content.replace('sec_title("🟡 Medium Risk"', 'sec_title("Medium Risk"')
    content = content.replace('sec_title("🟢 Low Risk"', 'sec_title("Low Risk"')
    content = content.replace('sec_title("👥 Risk Level by Patient Tier"', 'sec_title("Risk Level by Patient Tier"')
    content = content.replace('sec_title("🔥 Patient Engagement Status"', 'sec_title("Patient Engagement Status"')
    content = content.replace('sec_title("📋 Average Profile by Risk Category"', 'sec_title("Average Profile by Risk Category"')
    content = content.replace('sec_title("🚨 Top 20 High-Risk Patients — Prioritise for Outreach")', 'sec_title("Top 20 High-Risk Patients — Prioritise for Outreach")')
    content = content.replace('sec_title("📅 Monthly Acquisition Cohorts"', 'sec_title("Monthly Acquisition Cohorts"')
    content = content.replace('sec_title("🧬 ML Patient Segments"', 'sec_title("ML Patient Segments"')
    content = content.replace('sec_title("📈 Nominal vs Real Revenue Over Time"', 'sec_title("Nominal vs Real Revenue Over Time"')
    content = content.replace('sec_title("📊 Revenue Index — Nominal vs Real (Base = 100)"', 'sec_title("Revenue Index — Nominal vs Real (Base = 100)"')
    content = content.replace('sec_title("🔥 Monthly Inflation Erosion"', 'sec_title("Monthly Inflation Erosion"')
    content = content.replace('sec_title("🔮 3-Month Visit Forecast"', 'sec_title("3-Month Visit Forecast"')
    content = content.replace('sec_title("🩺 Diabetes Prevalence by Age Group")', 'sec_title("Diabetes Prevalence by Age Group")')
    content = content.replace('sec_title("❤️ Hypertension Prevalence by Age Group")', 'sec_title("Hypertension Prevalence by Age Group")')
    content = content.replace('sec_title("🔥 Comorbidity Heatmap"', 'sec_title("Comorbidity Heatmap"')
    content = content.replace('sec_title("⚕️ Clinical Risk Factor Analysis"', 'sec_title("Clinical Risk Factor Analysis"')
    content = content.replace('sec_title("🔍 Data Quality Dashboard"', 'sec_title("Data Quality Dashboard"')
    content = content.replace('sec_title("💰 Revenue Gap by Contract"', 'sec_title("Revenue Gap by Contract"')
    content = content.replace('sec_title("🏆 Top 15 Doctors by Referrals")', 'sec_title("Top 15 Doctors by Referrals")')
    content = content.replace('sec_title("🩺 Referrals by Specialty")', 'sec_title("Referrals by Specialty")')
    content = content.replace('sec_title("📊 Visits vs Revenue per Visit by Branch")', 'sec_title("Visits vs Revenue per Visit by Branch")')
    content = content.replace('sec_title("🕸️ Branch Performance Radar")', 'sec_title("Branch Performance Radar")')
    content = content.replace('sec_title("⚔️ Branch vs Branch Comparison"', 'sec_title("Branch vs Branch Comparison"')
    content = content.replace('sec_title("📊 Side-by-Side Comparison"', 'sec_title("Side-by-Side Comparison"')
    content = content.replace('sec_title("📊 Executive Summary Report")', 'sec_title("Executive Summary Report")')
    content = content.replace('sec_title("🛠️ Custom Report Builder")', 'sec_title("Custom Report Builder")')
    content = content.replace('sec_title("Referral Flow by Branch & Specialty")', 'sec_title("Referral Flow by Branch & Specialty")')

    # Info card titles
    content = content.replace('info_card_start("🔎 Advanced Filters")', 'info_card_start("Advanced Filters")')
    content = content.replace('info_card_start("Patient Information")', 'info_card_start("Patient Information")')
    content = content.replace('info_card_start("All Doctors Performance")', 'info_card_start("All Doctors Performance")')
    content = content.replace('info_card_start("Contract Details")', 'info_card_start("Contract Details")')
    content = content.replace('info_card_start("All Corporate Contracts")', 'info_card_start("All Corporate Contracts")')
    content = content.replace('info_card_start("All Contracts — Utilization Overview")', 'info_card_start("All Contracts — Utilization Overview")')
    content = content.replace('info_card_start("Branch Flow Summary")', 'info_card_start("Branch Flow Summary")')
    content = content.replace('info_card_start("Branch Flow Analysis")', 'info_card_start("Branch Flow Analysis")')
    content = content.replace('info_card_start("Branch Scorecard Table")', 'info_card_start("Branch Scorecard Table")')
    content = content.replace('info_card_start("Tier Metrics Table")', 'info_card_start("Tier Metrics Table")')
    content = content.replace('info_card_start("Metric Comparison Table")', 'info_card_start("Metric Comparison Table")')
    content = content.replace('info_card_start("Detailed Quality Report")', 'info_card_start("Detailed Quality Report")')
    content = content.replace('info_card_start("📋 Tier Metrics Table")', 'info_card_start("Tier Metrics Table")')
    content = content.replace('info_card_start("📋 Metric Comparison Table")', 'info_card_start("Metric Comparison Table")')
    content = content.replace('info_card_start("📋 Branch Scorecard Table")', 'info_card_start("Branch Scorecard Table")')
    content = content.replace('info_card_start("📅 Detailed Monthly Forecast")', 'info_card_start("Detailed Monthly Forecast")')

    # KPI card icons - replace with empty string
    content = content.replace('icon="👥"', 'icon=""')
    content = content.replace('icon="📊"', 'icon=""')
    content = content.replace('icon="👨‍⚕️"', 'icon=""')
    content = content.replace('icon="⚠️"', 'icon=""')
    content = content.replace('icon="📈"', 'icon=""')
    content = content.replace('icon="🏆"', 'icon=""')
    content = content.replace('icon="⭐"', 'icon=""')
    content = content.replace('icon="📅"', 'icon=""')
    content = content.replace('icon="🩺"', 'icon=""')
    content = content.replace('icon="💰"', 'icon=""')
    content = content.replace('icon="✅"', 'icon=""')
    content = content.replace('icon="❤️"', 'icon=""')
    content = content.replace('icon="📉"', 'icon=""')
    content = content.replace('icon="🚀"', 'icon=""')
    content = content.replace('icon="🔥"', 'icon=""')
    content = content.replace('icon="💵"', 'icon=""')
    content = content.replace('icon="🏦"', 'icon=""')
    content = content.replace('icon="📱"', 'icon=""')
    content = content.replace('icon="❌"', 'icon=""')
    content = content.replace('icon="💸"', 'icon=""')
    content = content.replace('icon="🥇"', 'icon=""')
    content = content.replace('icon="🥈"', 'icon=""')
    content = content.replace('icon="🥉"', 'icon=""')
    content = content.replace('icon="🔴"', 'icon=""')
    content = content.replace('icon="🟡"', 'icon=""')
    content = content.replace('icon="🟢"', 'icon=""')
    content = content.replace('icon="🚨"', 'icon=""')
    content = content.replace('icon="⚠️"', 'icon=""')
    content = content.replace('icon="🏥"', 'icon=""')
    content = content.replace('icon="📋"', 'icon=""')
    content = content.replace('icon="🗄️"', 'icon=""')
    content = content.replace('icon="🔁"', 'icon=""')
    content = content.replace('icon="⏱️"', 'icon=""')
    content = content.replace('icon="⚔️"', 'icon=""')

    # Button labels
    content = content.replace('st.button("🔍 Search"', 'st.button("Search"')
    content = content.replace('st.button("🔎 Apply Filters"', 'st.button("Apply Filters"')
    content = content.replace('st.button("↺ Refresh Data"', 'st.button("Refresh Data"')
    content = content.replace('st.button("📥 Generate Full Report"', 'st.button("Generate Full Report"')
    content = content.replace('st.button("📥 Build Custom Report"', 'st.button("Build Custom Report"')

    # Download button labels
    content = content.replace('st.download_button("📊 Download Excel"', 'st.download_button("Download Excel"')
    content = content.replace('st.download_button("📄 Download CSV"', 'st.download_button("Download CSV"')
    content = content.replace('st.download_button("📊 Export Results"', 'st.download_button("Export Results"')
    content = content.replace('st.download_button("📊 Export Doctors"', 'st.download_button("Export Doctors"')
    content = content.replace('st.download_button("📊 Export Contracts"', 'st.download_button("Export Contracts"')
    content = content.replace('st.download_button("📊 Export Gap Analysis"', 'st.download_button("Export Gap Analysis"')
    content = content.replace('st.download_button("📊 Export At-Risk List"', 'st.download_button("Export At-Risk List"')
    content = content.replace('st.download_button("📊 Export High-Risk List"', 'st.download_button("Export High-Risk List"')
    content = content.replace('st.download_button("📊 Export Branch Scorecard"', 'st.download_button("Export Branch Scorecard"')
    content = content.replace('st.download_button("📊 Export Tier Analysis"', 'st.download_button("Export Tier Analysis"')
    content = content.replace('st.download_button("📥 Download Excel Report"', 'st.download_button("Download Excel Report"')
    content = content.replace('st.download_button("📥 Download Custom Report"', 'st.download_button("Download Custom Report"')
    content = content.replace('st.download_button("📄 Download PDF Report"', 'st.download_button("Download PDF Report"')
    content = content.replace('st.download_button("📊 Download as Excel"', 'st.download_button("Download as Excel"')
    content = content.replace('st.download_button("📄 Download as CSV"', 'st.download_button("Download as CSV"')

    # Success/error messages
    content = content.replace('st.success(f"✅ Patient Found:', 'st.success(f"Patient Found:')
    content = content.replace('st.success(f"✅ Doctor Found:', 'st.success(f"Doctor Found:')
    content = content.replace('st.success(f"✅ Contract Found:', 'st.success(f"Contract Found:')
    content = content.replace('st.success(f"✅ Report generated successfully!")', 'st.success(f"Report generated successfully!")')
    content = content.replace('st.success(f"✅ Custom report generated with {len(selected)} sheets!")', 'st.success(f"Custom report generated with {len(selected)} sheets!")')
    content = content.replace('st.success("✅ No at-risk doctors detected!")', 'st.success("No at-risk doctors detected!")')
    content = content.replace('st.success("✅ No missing values in this table!")', 'st.success("No missing values in this table!")')

    content = content.replace('st.error(f"❌ Patient ID \'{patient_id}\' not found!")', 'st.error(f"Patient ID \'{patient_id}\' not found!")')
    content = content.replace('st.error(f"❌ Doctor ID \'{doctor_id}\' not found!")', 'st.error(f"Doctor ID \'{doctor_id}\' not found!")')
    content = content.replace('st.error(f"❌ Corporate ID \'{corp_id}\' not found!")', 'st.error(f"Corporate ID \'{corp_id}\' not found!")')

    # Warning messages
    content = content.replace('st.warning("⚠️ Need ≥ 2 months of data to compute CAGR.")', 'st.warning("Need at least 2 months of data to compute CAGR.")')
    content = content.replace('st.warning("Please select at least one data source")', 'st.warning("Please select at least one data source")')

    # Info messages
    content = content.replace('st.info("📊 Building revenue analysis from visits data...")', 'st.info("Building revenue analysis from visits data...")')
    content = content.replace('st.info(f"📌 **Inflation Note:** Real CAGR = **{cagr_real:+.1f}%** after Egypt\'s ~{INFL*100:.0f}%/yr inflation")', 'st.info(f"Inflation Note: Real CAGR = {cagr_real:+.1f}% after Egypt\'s ~{INFL*100:.0f}%/yr inflation")')
    content = content.replace('st.info("Need more patients for segmentation analysis")', 'st.info("Need more patients for segmentation analysis")')
    content = content.replace('st.info("Need at least 2 months of data for forecasting")', 'st.info("Need at least 2 months of data for forecasting")')

    # Footer emojis
    content = content.replace('📱 <a href="https://wa.me/201143575727"', 'Phone: <a href="https://wa.me/201143575727"')
    content = content.replace('📧 <a href="mailto:ahmdsa1@proton.com"', 'Email: <a href="mailto:ahmdsa1@proton.com"')

    # HTML content in sidebar
    content = content.replace('● Data refreshed', 'Data refreshed')

    # Clean up any double spaces left behind
    content = content.replace('  ', ' ')
    content = content.replace('  ', ' ')

    return content

def main():
    print("Reading app.py...")
    content = read_file('app.py')

    print("Removing emojis...")
    content = remove_emojis(content)

    print("Writing updated app.py...")
    write_file('app.py', content)
    print("✅ Done!")

if __name__ == "__main__":
    main()

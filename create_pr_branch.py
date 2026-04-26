#!/usr/bin/env python3
"""
Create a new git branch for the PR and commit all tracked changes.
"""
import subprocess
import sys

def run(cmd, **kwargs):
    print(f"$ {cmd}")
    result = subprocess.run(cmd.split(), shell=True, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print(f"STDERR: {result.stderr}")
    print(f"STDOUT: {result.stdout}")
    return result

# Create and switch to new branch
branch_name = "blackboxai/phase-1-dashboard-improvements"
print("Step 1: Creating branch...")
run(f"git branch -D {branch_name}")  # Delete if exists
run(f"git checkout -b {branch_name}")

# Stage all tracked files clean-up
tracked = ["alerts.py", "app.py", "reports.py"]
for f in tracked:
    run(f"git add {f}")
run(f"git rm -f seed_doctors_corporates.py")

# Commit
print("Step 2: Committing...")
result = run(f'git commit -m "feat(dashboard): Phase 1 – 10 feature improvements\n\nFeatures added:\n1. Global Date Range Filter (sidebar)\n2. Data Freshness Indicator (sidebar refresh)\n3. Doctor Ranking Dashboard page\n4. Corporate Utilization Gap analysis\n5. Day-of-Week × Hour heatmap\n6. Branch Operational Scorecard\n7. No-Show Cost Estimator\n8. Revenue Per Patient Tier analysis\n9. Patient Retention Cohort Table\n10. PDF Report Export"')

print("Step 3: Done!")
print(result.stdout)
print(result.stderr)

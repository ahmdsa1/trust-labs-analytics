# Trust Labs Analytics Dashboard — Phase 1 Implementation Tracker

## Features to Implement (in order)

- [ ] **Feature 1**: Global Date Range Filter (Sidebar)
- [ ] **Feature 2**: Data Freshness Indicator (Sidebar)
- [ ] **Feature 3**: Doctor Ranking Dashboard (New Page)
- [ ] **Feature 4**: Corporate Utilization Gap Table
- [ ] **Feature 5**: Day-of-Week × Hour Heatmap
- [ ] **Feature 6**: Branch Operational Scorecard
- [ ] **Feature 7**: No-Show Cost Estimator
- [ ] **Feature 8**: Revenue Per Patient Tier
- [ ] **Feature 9**: Patient Retention Cohort Table
- [ ] **Feature 10**: PDF Report Export

## Files to Edit

| File | Features |
|------|----------|
| `app.py` | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| `alerts.py` | 3 |
| `reports.py` | 10 |
| `requirements.txt` | 10 |

## Validation Checklist (per feature)

- [ ] Renders without errors on admin login
- [ ] Renders without errors on viewer login
- [ ] Handles empty DataFrames gracefully
- [ ] Respects global date filter (Feature 1)
- [ ] Matches visual style (fonts, colors, card styles)
- [ ] `py_compile` passes with no syntax errors
- [ ] Admin-only features hidden from viewer role

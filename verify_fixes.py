#!/usr/bin/env python3
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'Branch Flow uses doctor_branch': 'doctor_branch = pd.read_sql' in content,
    'Revenue Mix uses visits_data directly': 'visits_data.groupby("patient_tier")' in content,
    'No emojis in navigation': '"Home"' in content and '"Analytics"' in content,
    'No emojis in kpi_card': 'icon=""' in content,
    'Branch Ops has debug warnings': 'No branch data available' in content,
}

for name, result in checks.items():
    status = 'PASS' if result else 'FAIL'
    print(f'{status}: {name}')

# Count remaining emojis
import re
emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]+", flags=re.UNICODE)
emojis = emoji_pattern.findall(content)
if emojis:
    print(f'WARNING: {len(emojis)} emoji sequences still found')
    # Show unique ones
    unique = set()
    for e in emojis:
        unique.add(e)
    print(f'Unique emojis remaining: {sorted(unique)[:10]}')  # Show first 10
else:
    print('PASS: No emojis remaining')

#!/usr/bin/env python3
"""
Remove emoji characters from app.py without affecting indentation
"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Emoji regex pattern - matches emoji codepoints
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "]+",
    flags=re.UNICODE
)

# Remove emojis only - do NOT touch spaces/indentation
cleaned = emoji_pattern.sub('', content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(cleaned)

# Verify
remaining = emoji_pattern.findall(cleaned)
if remaining:
    print(f"WARNING: {len(remaining)} emoji sequences still found")
else:
    print("All emojis removed successfully")

#!/usr/bin/env python3
"""
Remove all emoji characters from app.py using regex
Preserves code structure and non-emoji Unicode characters
"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Emoji regex pattern - matches emoji codepoints but not box-drawing or other symbols
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols
    "\U0001FA70-\U0001FAFF"  # symbols extended-a
    "\U00002600-\U000026FF"  # miscellaneous symbols
    "\U00002700-\U000027BF"  # dingbats
    "]+",
    flags=re.UNICODE
)

# Remove emojis
cleaned = emoji_pattern.sub('', content)

# Clean up double spaces left by emoji removal
cleaned = re.sub(r'  +', ' ', cleaned)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(cleaned)

# Verify
remaining = emoji_pattern.findall(cleaned)
if remaining:
    unique = sorted(set(''.join(remaining)))
    print(f"WARNING: {len(remaining)} emoji sequences still found")
    print(f"Unique: {unique[:20]}")
else:
    print("All emojis removed successfully")

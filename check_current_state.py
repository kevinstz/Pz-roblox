import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

ref = "R133861"
idx = text.find(f'referent="{ref}"')
print(f"Found {ref} at {idx}")
if idx != -1:
    end_idx = text.find("</Item>", idx)
    print(text[idx:end_idx+7])

# Let's search for "walls_commercial"
commercial_matches = re.findall(r'<string name="Name">(walls_commercial_[^<]+)</string>', text)
print(f"\nTotal walls_commercial parts remaining: {len(commercial_matches)}")
from collections import Counter
print(Counter(commercial_matches))

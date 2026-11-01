import re
from collections import Counter

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
prefixes = Counter()

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m = re.search(r'<UniqueId name="UniqueId">([0-9a-fA-F]{24})([0-9a-fA-F]{8})</UniqueId>', line)
        if m:
            prefixes[m.group(1).lower()] += 1

for p, c in prefixes.most_common():
    print(f"{p}: {c}")

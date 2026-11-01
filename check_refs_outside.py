import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

refs_before = set()
refs_after = set()

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f, 1):
        if idx < 50439:
            m = re.search(r'referent="([^"]+)"', line)
            if m:
                refs_before.add(m.group(1))
        elif idx > 1999387:
            m = re.search(r'referent="([^"]+)"', line)
            if m:
                refs_after.add(m.group(1))

print(f"Referents before: {len(refs_before)}")
print(f"Referents after: {len(refs_after)}")

# Check numeric ranges in refs_after
num_after = []
for r in refs_after:
    if r.startswith('R') and r[1:].isdigit():
        num_after.append(int(r[1:]))

print(f"Numeric referents after: min={min(num_after)}, max={max(num_after)}")

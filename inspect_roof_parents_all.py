import re
from collections import defaultdict

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Group roofs by parent Model in Exterior or elsewhere
# Find all <string name="Name">roof...
roof_matches = list(re.finditer(r'<string name="Name">(roof[s]?_[^<]+)</string>', text, re.IGNORECASE))
print(f"Total roof matches: {len(roof_matches)}")

bld_roofs = defaultdict(list)
for m in roof_matches:
    idx = m.start()
    name = m.group(1)
    # find parent model
    p_pos = text.rfind('<Item class="Model"', 0, idx)
    p_name_m = re.search(r'<string name="Name">([^<]+)</string>', text[p_pos:p_pos+2500])
    p_name = p_name_m.group(1) if p_name_m else "Unknown"
    
    # find position
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text[item_start:idx], re.DOTALL)
    pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else (0,0,0)
    
    bld_roofs[p_name].append((name, pos))

print("\nRoofs grouped by Model:")
for p_name, rlist in sorted(bld_roofs.items(), key=lambda x: len(x[1]), reverse=True):
    xs = [r[1][0] for r in rlist]
    zs = [r[1][2] for r in rlist]
    print(f"  {p_name:30s} ({len(rlist)} roofs) | X=[{min(xs):.1f}..{max(xs):.1f}], Z=[{min(zs):.1f}..{max(zs):.1f}]")

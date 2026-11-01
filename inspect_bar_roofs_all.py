import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Inspect Exterior_8080_11648
idx = text.find('<string name="Name">Exterior_8080_11648</string>')
item_start = text.rfind('<Item class="Model"', 0, idx)
# find next Model at level 4 (\t\t\t\t<Item class="Model")
next_model = text.find('\n\t\t\t\t<Item class="Model"', idx)
chunk = text[item_start:next_model]

matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', chunk, re.DOTALL)
roofs = []
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        name = m_name.group(1)
        if 'roof' in name.lower():
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            roofs.append((ref, name, cls, x, y, z, sz, m_tex))

print(f"Total roofs in Exterior_8080_11648: {len(roofs)}")
from collections import Counter
print("Roof types in Exterior_8080_11648:", Counter([r[1] for r in roofs]))

# Print roofs grouped by Y level
by_y = {}
for r in roofs:
    y_round = round(r[4], 1)
    if y_round not in by_y: by_y[y_round] = []
    by_y[y_round].append(r)

for y_val in sorted(by_y.keys()):
    rlist = by_y[y_val]
    xs = [r[3] for r in rlist]
    zs = [r[5] for r in rlist]
    print(f"\n--- Y = {y_val} ({len(rlist)} parts) ---")
    print(f"  Types: {dict(Counter([r[1] for r in rlist]))}")
    print(f"  X bounds: [{min(xs):.1f} .. {max(xs):.1f}], Z bounds: [{min(zs):.1f} .. {max(zs):.1f}]")
    for r in rlist[:5]:
        print(f"    {r[0]:8s} | {r[1]:24s} | Pos=({r[3]:6.2f}, {r[4]:6.2f}, {r[5]:6.2f}) | Size={r[6]} | Tex={r[7]}")

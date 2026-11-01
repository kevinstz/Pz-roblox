# Let's check hedge positions and car positions
import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find hedges
hedges = []
for m in re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    if m_name and 'hedge' in m_name.group(1).lower() or (m_name and 'bush' in m_name.group(1).lower()) or (m_name and 'f_bushes' in m_name.group(1).lower()):
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            hedges.append((ref, m_name.group(1), x, y, z))

print(f"Total hedges: {len(hedges)}")

# Check distance from each car pair:
pairs = [
    ("Pair 1 (-78, -138) / (-57, -138)", -67, -138),
    ("Pair 2 (-21, -60) / (-21, -36)", -21, -48),
    ("Pair 3 (69, -66) / (90, -66)", 80, -66),
    ("Pair 4 (153, -150) / (153, -120)", 153, -135),
]

for name, cx, cz in pairs:
    nearby_hedges = [h for h in hedges if abs(h[2] - cx) < 30 and abs(h[4] - cz) < 30]
    print(f"{name}: {len(nearby_hedges)} hedges nearby")
    for h in nearby_hedges[:5]:
        print(f"   {h[1]} at ({h[2]:.1f}, {h[3]:.1f}, {h[4]:.1f})")

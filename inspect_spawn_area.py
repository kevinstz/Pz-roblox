import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's check all models and objects within 100 studs of spawn (X in [50, 200], Z in [80, 250])
# Find all parts with roof in name in this area:
roofs_near_spawn = []
doors_near_spawn = []
walls_near_spawn = []

# Scan all parts in PZ_Rosewood
matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
    m_cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', block)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        name = m_name.group(1)
        cc = m_cc.group(1) if m_cc else "unknown"
        if 50 <= x <= 200 and 80 <= z <= 250:
            if 'roof' in name.lower():
                roofs_near_spawn.append((ref, name, cls, x, y, z, cc))
            elif 'door' in name.lower() or 'puerta' in name.lower():
                doors_near_spawn.append((ref, name, cls, x, y, z, cc))
            elif 'wall' in name.lower() and cc == 'false':
                walls_near_spawn.append((ref, name, cls, x, y, z, cc))

print(f"Near spawn (129, 168):")
print(f"  Roofs: {len(roofs_near_spawn)}")
from collections import Counter
print("  Roof types:", Counter([r[1] for r in roofs_near_spawn]))
print(f"  Doors: {len(doors_near_spawn)}")
print("  Doors CanCollide false:", [d[1] for d in doors_near_spawn if d[6] == 'false'])
print(f"  Walls CanCollide false: {len(walls_near_spawn)}")
print("  Walls CanCollide false types:", Counter([w[1] for w in walls_near_spawn]))

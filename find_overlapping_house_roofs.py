import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect old roof parts in Exterior that overlap with the 3 houses:
# House 28: X in [175, 190], Z in [-250, -218]
# House 33: X in [145, 170], Z in [8, 40]
# House 22: X in [100, 120], Z in [-185, -150]

houses = [
    ("House 28", 175, 190, -250, -218),
    ("House 33", 145, 170, 8, 40),
    ("House 22", 100, 120, -185, -150)
]

for hname, x_min, x_max, z_min, z_max in houses:
    print(f"\n=== Overlapping parts for {hname} ===")
    matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
    for m in matches:
        cls, ref, block = m.group(1), m.group(2), m.group(3)
        # only check if it's not one of our new parts (ref >= 200000)
        if ref.startswith('R200'):
            continue
        m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        if m_cf and m_name:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if x_min <= x <= x_max and z_min <= z <= z_max and y >= 6.0:
                name = m_name.group(1)
                if 'roof' in name.lower() or 'wall' in name.lower():
                    print(f"  {ref:8s} | {cls:8s} | {name:30s} | Pos=({x:6.2f}, {y:6.2f}, {z:6.2f})")

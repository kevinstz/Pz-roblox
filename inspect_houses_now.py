import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# House 28 bounds: X in [175, 190], Z in [-250, -218]
# House 33 bounds: X in [145, 170], Z in [8, 40]
# House 22 bounds: X in [100, 120], Z in [-185, -150]

for hname, x_min, x_max, z_min, z_max in [
    ("House 28", 175, 190, -250, -218),
    ("House 33", 145, 170, 8, 40),
    ("House 22", 100, 120, -185, -150)
]:
    print(f"\n=== {hname} ===")
    matches = list(re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL))
    parts = []
    for m in matches:
        cls, ref, b = m.group(1), m.group(2), m.group(3)
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', b, re.DOTALL)
        m_n = re.search(r'<string name="Name">([^<]+)</string>', b)
        m_cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', b)
        if m_cf and m_n:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if x_min <= x <= x_max and z_min <= z <= z_max and y >= 6.0:
                name = m_n.group(1)
                cc = m_cc.group(1) if m_cc else "unknown"
                parts.append((ref, name, cls, x, y, z, cc))
    print(f"Parts at roof level (Y >= 6.0): {len(parts)}")
    for p in parts:
        print(f"  {p[0]:8s} | {p[2]:10s} | {p[1]:30s} | Pos=({p[3]:.1f}, {p[4]:.1f}, {p[5]:.1f}) | CanCollide={p[6]}")

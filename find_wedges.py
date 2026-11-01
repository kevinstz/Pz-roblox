# Find all WedgePart in PZ_Rosewood.rbxlx near X in [-55, -40], Z in [-80, -60]
with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

wedges = []
for m in re.finditer(r'<Item class="(WedgePart|CornerWedgePart)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    block = m.group(0)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    if m_cf:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -60 <= x <= -40 and -80 <= z <= -55:
            m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
            name = m_name.group(1) if m_name else "?"
            m_s = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
            sz = f"({float(m_s.group(1)):.2f}, {float(m_s.group(2)):.2f}, {float(m_s.group(3)):.2f})" if m_s else "?"
            wedges.append((m.group(2), m.group(1), name, (x, y, z), sz))

print(f"Total wedges in area: {len(wedges)}")
for w in wedges:
    print(f"Ref={w[0]} | Cls={w[1]} | Name={w[2]:25s} | pos=({w[3][0]:.2f}, {w[3][1]:.2f}, {w[3][2]:.2f}) | sz={w[4]}")

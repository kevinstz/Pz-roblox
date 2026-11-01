import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# House 28: Livingroom_31_45_28 is at X: [178..188], Z: [-248..-220]
# House 33: Livingroom_31_45_33 is at X: [148..167], Z: [10..38]
# House 22: Derelict_31_45_22 is at X: [106..116], Z: [-180..-155]

for hname, x_min, x_max, z_min, z_max in [
    ("House 28", 175, 190, -250, -218),
    ("House 33", 145, 170, 8, 40),
    ("House 22", 100, 120, -185, -150)
]:
    print(f"\n=== Checking {hname} ===")
    # Find all parts with 'roof' in name within bounds
    # We can search for <Item class="Part"... or WedgePart
    pos = 0
    roof_parts = []
    while True:
        idx = text.find('<string name="Name">', pos)
        if idx == -1: break
        idx_end = text.find('</string>', idx)
        name = text[idx+20:idx_end]
        if 'roof' in name.lower():
            item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
            item_end = text.find('</Item>', idx)
            block = text[item_start:item_end]
            m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
            if m_cf:
                x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
                if x_min <= x <= x_max and z_min <= z <= z_max:
                    m_cls = re.search(r'<Item class="([^"]+)"', block)
                    cls = m_cls.group(1) if m_cls else 'Part'
                    m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
                    sz = m_sz.groups() if m_sz else ()
                    roof_parts.append((name, cls, x, y, z, sz))
        pos = idx_end
    print(f"Found {len(roof_parts)} roof parts:")
    for r in roof_parts:
        print(f"  {r[0]:30s} | {r[1]:10s} | Pos=({r[2]:.1f}, {r[3]:.1f}, {r[4]:.1f}) | Sz={r[5]}")

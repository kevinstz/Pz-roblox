import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find every part in the building X in [-60, -35], Z in [-80, -15], Y in [2, 28]
# that has any 'walls_commercial' or color in [4284049516, 4284838261, 4289243802, 4292072640]
matches = re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
bld_defects = []
for m in matches:
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        name = m_name.group(1)
        col = m_col.group(1) if m_col else ''
        if -60 <= x <= -35 and -85 <= z <= -15 and y >= 2.0:
            if 'walls_commercial' in name or col in ['4284049516', '4284838261', '4289243802']:
                bld_defects.append({
                    'ref': ref, 'name': name, 'pos': (x, y, z), 'col': col, 'tex': m_tex
                })

print(f"Total commercial/cyan wall parts on this building: {len(bld_defects)}")
# Group by wall face / orientation
# North/South walls (X varies, Z fixed, Size.X >= Size.Z)
# East/West walls (Z varies, X fixed, Size.Z >= Size.X)
for p in bld_defects:
    print(f"Ref={p['ref']:8s} | Name={p['name']:30s} | Pos=({p['pos'][0]:6.2f}, {p['pos'][1]:6.2f}, {p['pos'][2]:6.2f}) | Col={p['col']:10s} | Tex={p['tex']}")

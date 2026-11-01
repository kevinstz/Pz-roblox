import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all parts in Bar_31_45_12 and all Exterior models around X in [-60, -35], Z in [-80, -10]
# that have commercial wall tiles or pale cyan/white colors:
matches = re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)

defects = []
for m in matches:
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        name = m_name.group(1)
        col = m_col.group(1) if m_col else ''
        
        # Check if in the building area:
        if -60 <= x <= -35 and -85 <= z <= -15 and y >= 2.0:
            # Check if it's a pale/cyan/white wall panel or commercial wall
            is_defect = False
            if 'walls_commercial' in name:
                is_defect = True
            elif col in ['4284049516', '4284838261', '4289243802']:
                is_defect = True
            elif any('67cf' in t or '37ee' in t for t in m_tex):
                is_defect = True
            
            if is_defect:
                defects.append((ref, name, (x, y, z), col, m_tex))

print(f"Total defective/commercial wall parts in building: {len(defects)}")
defects.sort(key=lambda p: (p[2][1], p[2][2], p[2][0])) # sort by Y, then Z, then X
for p in defects:
    print(f"Ref={p[0]:8s} | Name={p[1]:30s} | Pos=({p[2][0]:6.2f}, {p[2][1]:6.2f}, {p[2][2]:6.2f}) | Col={p[3]:10s} | Tex={p[4]}")

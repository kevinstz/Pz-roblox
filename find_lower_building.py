import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Search near (-31, -26):
matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
near_roof = []
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -38 <= x <= -20 and -35 <= z <= -15 and 3.0 <= y <= 15.0:
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            near_roof.append({
                'ref': ref, 'cls': cls, 'name': m_name.group(1),
                'pos': (x, y, z), 'size': sz, 'col': m_col.group(1) if m_col else '',
                'tex': m_tex
            })

print(f"Total parts near (-31, -26): {len(near_roof)}")
near_roof.sort(key=lambda p: (p['pos'][1], p['pos'][2], p['pos'][0]))
for p in near_roof:
    print(f"Ref={p['ref']:8s} | Cls={p['cls']:8s} | Name={p['name']:32s} | Pos=({p['pos'][0]:6.2f}, {p['pos'][1]:6.2f}, {p['pos'][2]:6.2f}) | Size={p['size']} | Col={p['col']:10s} | Tex={p['tex']}")

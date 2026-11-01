import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all parts in this roof area:
# In crop_v4_lower_left_roof.jpg:
# Pos is roughly X in [-52, -44], Z in [-75, -60], Y in [4, 12]
matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
roof_parts = []
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_rot = re.search(r'<R01>([^<]+)</R01>.*?<R02>([^<]+)</R02>.*?<R10>([^<]+)</R10>', block, re.DOTALL)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -52 <= x <= -44 and -75 <= z <= -60 and 4.0 <= y <= 12.0:
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            roof_parts.append({
                'cls': cls, 'ref': ref, 'name': m_name.group(1),
                'pos': (x, y, z), 'col': m_col.group(1) if m_col else '',
                'sz': sz, 'tex': m_tex
            })

print(f"Total parts in lower left roof area: {len(roof_parts)}")
roof_parts.sort(key=lambda p: (p['pos'][1], p['pos'][2], p['pos'][0]))
for p in roof_parts:
    print(f"Ref={p['ref']:8s} | Cls={p['cls']:8s} | Name={p['name']:30s} | Pos=({p['pos'][0]:6.2f}, {p['pos'][1]:6.2f}, {p['pos'][2]:6.2f}) | Size={p['sz']} | Col={p['col']:10s} | Tex={p['tex']}")

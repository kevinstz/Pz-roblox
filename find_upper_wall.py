import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find ALL parts between X in [-48, -45], Z in [-70, -20], Y in [14, 23]
matches = re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
upper_wall = []
for m in matches:
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
    m_tex = re.findall(r'<url>([^<]+)</url>', block)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -50 <= x <= -44 and -70 <= z <= -20 and 14 <= y <= 23:
            upper_wall.append({
                'ref': ref, 'name': m_name.group(1),
                'pos': (x, y, z), 'col': m_col.group(1) if m_col else '',
                'tex': m_tex,
                'sz': (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            })

print(f"Total parts in upper wall region: {len(upper_wall)}")
upper_wall.sort(key=lambda p: (p['pos'][2], p['pos'][1])) # sort by Z, then Y
for p in upper_wall:
    print(f"Ref={p['ref']:8s} | Name={p['name']:30s} | Pos=({p['pos'][0]:6.2f}, {p['pos'][1]:6.2f}, {p['pos'][2]:6.2f}) | Col={p['col']:10s} | Tex={p['tex']}")

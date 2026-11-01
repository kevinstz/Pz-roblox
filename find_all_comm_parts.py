import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find all parts with 'walls_commercial' in their name
comm_parts = []
for m in re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    if m_name and 'walls_commercial' in m_name.group(1):
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
        m_tex = re.findall(r'<url>([^<]+)</url>', block)
        pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else None
        comm_parts.append((ref, m_name.group(1), pos, m_col.group(1) if m_col else '', m_tex))

print(f"Total walls_commercial parts: {len(comm_parts)}")
for p in comm_parts:
    print(f"Ref={p[0]:8s} | Name={p[1]:30s} | Pos={p[2]} | Col={p[3]:10s} | Tex={p[4]}")

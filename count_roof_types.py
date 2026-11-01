import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search all parts with 'roof' in their name
roof_parts = []
for m in re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    if m_name and 'roof' in m_name.group(1).lower():
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        m_tex = re.findall(r'<url>([^<]+)</url>', block)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            roof_parts.append((cls, ref, m_name.group(1), (x, y, z), sz, m_tex))

print(f"Total roof parts in place: {len(roof_parts)}")
from collections import Counter
names = Counter(p[2] for p in roof_parts)
for k, v in names.most_common(25):
    print(f"  {k:35s}: {v}")

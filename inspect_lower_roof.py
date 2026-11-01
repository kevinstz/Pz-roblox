import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('<string name="Name">Exterior_8080_11648</string>')
item_idx = text.rfind('<Item class="Model"', 0, idx)
next_model = text.find('<Item class="Model"', idx)
block = text[item_idx:next_model]

parts = re.findall(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', block, re.DOTALL)
roof_parts = []
for cls, ref, pblock in parts:
    m_name = re.search(r'<string name="Name">([^<]+)</string>', pblock)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', pblock, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', pblock)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -55 <= x <= -45 and -75 <= z <= -65 and 7 <= y <= 13:
            roof_parts.append((cls, ref, m_name.group(1), x, y, z, m_col.group(1) if m_col else ""))

roof_parts.sort(key=lambda item: (item[4], item[3]))
for p in roof_parts:
    print(f"Cls={p[0]:10s} | Ref={p[1]:8s} | Name={p[2]:30s} | Pos=({p[3]:.2f}, {p[4]:.2f}, {p[5]:.2f}) | Col={p[6]}")

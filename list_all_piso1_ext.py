import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('<string name="Name">Exterior_8080_11648</string>')
item_idx = text.rfind('<Item class="Model"', 0, idx)
# Find the next model at the same indentation level
next_model = text.find('<Item class="Model"', idx)
block = text[item_idx:next_model]

parts = re.findall(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', block, re.DOTALL)
print(f"Total parts in Exterior_8080_11648: {len(parts)}")
piso1_parts = []
for ref, pblock in parts:
    m_name = re.search(r'<string name="Name">([^<]+)</string>', pblock)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', pblock, re.DOTALL)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', pblock)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if 9.0 <= y <= 13.0:
            piso1_parts.append((ref, m_name.group(1), x, y, z, m_col.group(1) if m_col else ""))

piso1_parts.sort(key=lambda item: (item[4], item[2])) # sort by Z, then X
for p in piso1_parts:
    print(f"Ref={p[0]:8s} | Name={p[1]:30s} | Pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Col={p[5]}")

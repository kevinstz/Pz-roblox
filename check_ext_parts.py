import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('<string name="Name">Exterior_8080_11648</string>')
# find the Item tag before it
item_idx = text.rfind('<Item', 0, idx)
end_model = text.find('</Item>\n\t\t\t\t<Item', item_idx)
# or find end of Exterior_8080_11648
block = text[item_idx:item_idx+150000]

# find parts
parts = re.findall(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', block, re.DOTALL)
print(f"Parts found: {len(parts)}")
for ref, pblock in parts[:25]:
    m_name = re.search(r'<string name="Name">([^<]+)</string>', pblock)
    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', pblock)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', pblock, re.DOTALL)
    m_tex = re.findall(r'<url>([^<]+)</url>', pblock)
    name = m_name.group(1) if m_name else ""
    col = m_col.group(1) if m_col else ""
    pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else None
    print(f"{ref} | {name:30s} | Col={col:10s} | Pos={pos} | Tex={m_tex}")

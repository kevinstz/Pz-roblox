import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for ref in ['R136287', 'R136419']:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        # find preceding Model
        m_idx = text.rfind('<Item class="Model"', 0, idx)
        name_idx = text.find('<string name="Name">', m_idx)
        name_end = text.find('</string>', name_idx)
        print(f"{ref} parent model: {text[name_idx+20:name_end]}")

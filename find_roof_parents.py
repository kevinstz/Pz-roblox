import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for name in ['roofs_slope_west', 'roofs_ridge_cap', 'skirting_west']:
    idx = text.find(f'<string name="Name">{name}</string>')
    if idx != -1:
        # find preceding Model
        m_idx = text.rfind('<Item class="Model"', 0, idx)
        m_name_idx = text.find('<string name="Name">', m_idx)
        m_name_end = text.find('</string>', m_name_idx)
        parent_model = text[m_name_idx+20:m_name_end]
        
        # find outer model
        m_idx2 = text.rfind('<Item class="Model"', 0, m_idx)
        m_name_idx2 = text.find('<string name="Name">', m_idx2)
        m_name_end2 = text.find('</string>', m_name_idx2)
        outer_model = text[m_name_idx2+20:m_name_end2]
        
        print(f"{name} -> parent={parent_model} -> outer={outer_model}")

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
refs = ['R133861', 'R133876', 'R133882', 'R133891', 'R133897', 'R133963', 'R133966', 'R133969', 'R133987', 'R133990']
for ref in refs:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        end = text.find('</Item>', idx)
        block = text[idx:end+7]
        m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
        m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
        m_dec = re.findall(r'<url>([^<]+)</url>', block)
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else None
        print(f'{ref}: Name={m_name.group(1) if m_name else ""} Col={m_col.group(1) if m_col else ""} Pos={pos} Decals={m_dec}')

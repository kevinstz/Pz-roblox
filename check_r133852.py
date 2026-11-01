import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for ref in ['R133852', 'R133858']:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        end = text.find('</Item>', idx)
        block = text[idx:end+7]
        m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
        m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
        m_dec = re.findall(r'<url>([^<]+)</url>', block)
        print(f"{ref}: Name={m_name.group(1)} | Col={m_col.group(1)} | Dec={m_dec}")

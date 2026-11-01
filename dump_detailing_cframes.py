import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for ref in ['R133571', 'R133507', 'R133537', 'R131024']:
    idx = text.find(f'referent="{ref}"')
    if idx != -1:
        end = text.find('</Item>', idx)
        block = text[idx:end+7]
        m_cf = re.search(r'<CoordinateFrame name="CFrame">(.*?)</CoordinateFrame>', block, re.DOTALL)
        print(f"=== {ref} ===")
        print(m_cf.group(1).strip() if m_cf else "")

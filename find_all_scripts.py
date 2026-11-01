import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

scripts = re.findall(r'<Item class="(?:LocalScript|Script)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
print(f"Total scripts: {len(scripts)}")
for ref, block in scripts:
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    print(f"Script: Ref={ref} | Name={m_name.group(1) if m_name else ''}")

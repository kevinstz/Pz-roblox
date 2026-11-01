import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

for ref in ['R3', 'R39347', 'R116275', 'R153242']:
    idx = text.find(f'referent="{ref}"')
    m_name = re.search(r'<string name="Name">([^<]+)</string>', text[idx:idx+1200])
    print(f"Folder {ref}: {m_name.group(1) if m_name else 'Unknown'}")

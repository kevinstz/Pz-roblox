with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

# Find Models under Workspace
m_blds = re.findall(r'<Item class="Model" referent="([^"]+)">\s*<Properties>\s*.*?<string name="Name">([^<]+)</string>', text, re.DOTALL)
print(f"Total models: {len(m_blds)}")
for ref, name in m_blds[:40]:
    print(f"{ref}: {name}")

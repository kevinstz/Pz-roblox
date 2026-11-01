with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

m_blds = re.findall(r'<Item class="Model" referent="([^"]+)">\s*<Properties>\s*.*?<string name="Name">([^<]+)</string>', text, re.DOTALL)
for ref, name in m_blds:
    if not name.startswith("Chunk_") and not name.startswith("Piso_"):
        print(f"{ref}: {name}")

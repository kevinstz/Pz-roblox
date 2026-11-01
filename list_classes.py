with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
items = set(re.findall(r'<Item class="([^"]+)"', text))
print("All Item classes in place:", items)

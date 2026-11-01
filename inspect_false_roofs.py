import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

roof_matches = list(re.finditer(r'<string name="Name">([^<]*roof[^<]*)</string>', text, re.IGNORECASE))
false_roof_types = []

for m in roof_matches:
    idx = m.start()
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    item_props = text[item_start:idx]
    cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', item_props)
    if cc and cc.group(1) == "false":
        false_roof_types.append(m.group(1))

from collections import Counter
print("Roof parts with CanCollide=false:")
for k, v in Counter(false_roof_types).most_common(20):
    print(f"  {k:30s}: {v}")

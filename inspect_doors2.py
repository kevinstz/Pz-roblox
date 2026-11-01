import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect parts named "Puerta" or "fixtures_doors" or "walls"
door_matches = list(re.finditer(r'<string name="Name">(Puerta[^<]*|fixtures_doors[^<]*)</string>', text))
print(f"Total door parts: {len(door_matches)}")

for i, m in enumerate(door_matches[:20]):
    name = m.group(1)
    # find enclosing Item
    idx = m.start()
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    item_props = text[item_start:idx]
    cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', item_props)
    cc_val = cc.group(1) if cc else "MISSING"
    print(f"  [{i}] {name:30s} | CanCollide = {cc_val}")

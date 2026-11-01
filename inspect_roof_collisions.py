import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect all parts with "roof" in Name
roof_matches = list(re.finditer(r'<string name="Name">([^<]*roof[^<]*)</string>', text, re.IGNORECASE))
print(f"Total roof matches: {len(roof_matches)}")

false_roofs = 0
true_roofs = 0
for m in roof_matches:
    idx = m.start()
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    item_props = text[item_start:idx]
    cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', item_props)
    if cc and cc.group(1) == "false":
        false_roofs += 1
    elif cc and cc.group(1) == "true":
        true_roofs += 1

print(f"Roof collisions: CanCollide True = {true_roofs}, CanCollide False = {false_roofs}")

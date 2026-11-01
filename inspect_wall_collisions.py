import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect parts named "walls_"
wall_matches = list(re.finditer(r'<string name="Name">(walls_[^<]+)</string>', text))
print(f"Total wall parts: {len(wall_matches)}")

false_walls = []
true_walls = 0

for m in wall_matches:
    idx = m.start()
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    item_props = text[item_start:idx]
    cc = re.search(r'<bool name="CanCollide">([^<]+)</bool>', item_props)
    if cc and cc.group(1) == "false":
        false_walls.append(m.group(1))
    elif cc and cc.group(1) == "true":
        true_walls += 1

print(f"Wall stats: CanCollide True = {true_walls}, CanCollide False = {len(false_walls)}")
from collections import Counter
print("False walls breakdown:", Counter(false_walls).most_common(20))

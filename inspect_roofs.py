import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect where roofs_30_06_ or roofs_30_ or roofs_04_ are located!
part_matches = re.finditer(
    r'<Item class="([^"]+)" referent="([^"]+)">\s*<Properties>\s*<string name="Name">(roof[s]?_[^<]+)</string>.*?'
    r'<CoordinateFrame name="CFrame">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>',
    text, re.DOTALL
)

found = []
for m in part_matches:
    cls, ref, name, x, y, z = m.groups()
    x, y, z = float(x), float(y), float(z)
    found.append((name, ref, x, y, z))

print(f"Total roof parts found: {len(found)}")
# Let's cluster or group them by Z/X
from collections import defaultdict
by_name = defaultdict(list)
for name, ref, x, y, z in found:
    prefix = "_".join(name.split("_")[:3])
    by_name[prefix].append((x, y, z, ref, name))

for prefix, items in sorted(by_name.items()):
    xs = [it[0] for it in items]
    ys = [it[1] for it in items]
    zs = [it[2] for it in items]
    print(f"{prefix} ({len(items)} parts): X=[{min(xs):.1f}, {max(xs):.1f}], Y=[{min(ys):.1f}, {max(ys):.1f}], Z=[{min(zs):.1f}, {max(zs):.1f}]")

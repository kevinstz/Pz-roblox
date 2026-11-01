import re
from collections import Counter

wall_collide_false = Counter()
wall_collide_true = Counter()
RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"

with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    for line in fin:
        if not buffering:
            if '<Item class="Part"' in line or '<Item class="WedgePart"' in line:
                buffering = True
                depth = 1
                buffer = [line]
        else:
            buffer.append(line)
            if '<Item ' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    buffering = False
                    block = "".join(buffer)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
                    if m_name and 'wall' in m_name.group(1).lower():
                        name = m_name.group(1)
                        # strip off any trailing part
                        base = name.split('|')[0]
                        category = "_".join(base.split('_')[:3])
                        if '<bool name="CanCollide">false</bool>' in block:
                            wall_collide_false[category] += 1
                        else:
                            wall_collide_true[category] += 1
                    buffer = []

print("Walls CanCollide=FALSE:")
for k, v in wall_collide_false.most_common():
    print(f"  {k}: {v}")

print("\nWalls CanCollide=TRUE:")
for k, v in wall_collide_true.most_common():
    print(f"  {k}: {v}")

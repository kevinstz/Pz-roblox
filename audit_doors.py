import re
from collections import Counter

door_objects = Counter()
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
                    if m_name:
                        name = m_name.group(1).lower()
                        if any(w in name for w in ['door', 'puerta', 'garage', 'gate', 'porton']):
                            cancollide = '<bool name="CanCollide">true</bool>' in block or '<bool name="CanCollide">' not in block # Roblox default is true
                            door_objects[(m_name.group(1).split('|')[0], cancollide)] += 1
                    buffer = []

for (name, coll), count in door_objects.most_common(40):
    print(f"{name} | CanCollide={coll}: {count}")

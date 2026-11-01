import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    wedge_count = 0
    wedge_can_collide = 0
    for line in fin:
        if not buffering:
            if '<Item class="WedgePart"' in line:
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
                    wedge_count += 1
                    if '<bool name="CanCollide">true</bool>' in block or '<bool name="CanCollide">' not in block:
                        wedge_can_collide += 1
                    buffer = []

print(f"Total WedgeParts in map: {wedge_count}, with CanCollide=True: {wedge_can_collide}")

import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
count = 0
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    for line in fin:
        if not buffering:
            if '<Item class="Part"' in line:
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
                    if 'walls_commercial_01_48' in block and '684037041b29ec20554a.png' in block:
                        count += 1
                    buffer = []

print("Total walls_commercial_01_48 with 684037041b29ec20554a.png in whole map:", count)

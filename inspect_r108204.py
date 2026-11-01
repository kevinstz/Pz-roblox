import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    for line in fin:
        if not buffering:
            if '<Item class="Part" referent="R108204">' in line:
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
                    print(block)
                    break

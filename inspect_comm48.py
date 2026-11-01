import re

RBXLX_PATH = r"out\PZ_Rosewood.rbxlx"
with open(RBXLX_PATH, "r", encoding="utf-8", errors="ignore") as fin:
    buffering = False
    depth = 0
    buffer = []
    count = 0
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
                    if 'walls_commercial_01_48' in block and count < 3:
                        print("ITEM:", count)
                        for l in buffer:
                            if any(k in l for k in ['Name', 'size', 'CFrame', 'Texture', 'Color3', 'CanCollide']):
                                print("  ", l.strip())
                        count += 1
                    buffer = []

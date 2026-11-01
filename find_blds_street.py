# Find models with parts in X in [0, 80], Z in [-80, 0]
with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

# Find items
models_found = {}
for m in re.finditer(r'<Item class="Model" referent="([^"]+)">\s*<Properties>\s*.*?<string name="Name">([^<]+)</string>', text, re.DOTALL):
    ref = m.group(1)
    name = m.group(2)
    # search next 50000 chars for CFrames
    sub = text[m.start():m.start()+200000]
    cfs = re.findall(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', sub, re.DOTALL)
    if cfs:
        xs = [float(c[0]) for c in cfs]
        zs = [float(c[2]) for c in cfs]
        min_x, max_x = min(xs), max(xs)
        min_z, max_z = min(zs), max(zs)
        if (min_x <= 60 and max_x >= -20) and (min_z <= 0 and max_z >= -80):
            print(f"{name:30s} | X in [{min_x:.1f}, {max_x:.1f}] | Z in [{min_z:.1f}, {max_z:.1f}] | parts={len(cfs)}")

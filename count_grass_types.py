rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re
from collections import Counter

counts = Counter()
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    for line in f:
        if '<Item class="Part"' in line:
            cap = True
            buf = [line]
            continue
        if cap:
            buf.append(line)
            if '</Item>' in line:
                cap = False
                text = "".join(buf)
                if 'blends_grassoverlays_01_' in text:
                    msize = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                    if msize:
                        s = (round(float(msize.group(1)), 2), round(float(msize.group(2)), 2), round(float(msize.group(3)), 2))
                        counts[s] += 1

print("Counts by size:", counts)

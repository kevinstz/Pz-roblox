rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

count_grass = 0
sizes = set()
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    cap = False
    for line in f:
        if '<Item class="Part"' in line:
            cap = True
            lines = [line]
            continue
        if cap:
            lines.append(line)
            if '</Item>' in line:
                cap = False
                text = "".join(lines)
                if 'Name">blends_grassoverlays_01_' in text:
                    count_grass += 1
                    msize = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                    if msize:
                        sizes.add((float(msize.group(1)), float(msize.group(2)), float(msize.group(3))))

print(f"Total blends_grassoverlays parts: {count_grass}")
print(f"Sizes found: {sizes}")

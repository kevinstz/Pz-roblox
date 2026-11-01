rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

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
                if 'Name">TerrenoCircundante' in text:
                    my = re.search(r'<Y>([^<]+)</Y>', text)
                    msize = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                    mcol = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', text)
                    mmat = re.search(r'<token name="Material">([^<]+)</token>', text)
                    print(f"TerrenoCircundante Y={my.group(1)}, Size={msize.group(1)}, {msize.group(2)}, {msize.group(3)}, Col={mcol.group(1)}, Mat={mmat.group(1)}")
                    break

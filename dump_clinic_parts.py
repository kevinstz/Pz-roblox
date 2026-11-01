rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Clinic coordinates:
# OX = 8102.5, OY = 11672.5
# x in [8072, 8082] -> cx in [(8072 - 8102.5)*3, (8082 - 8102.5)*3] = [-91.5, -61.5]
# y in [11622, 11630] -> cz in [(11622 - 11672.5)*3, (11630 - 11672.5)*3] = [-151.5, -127.5]

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
                mx = re.search(r'<X>([^<]+)</X>', text)
                mz = re.search(r'<Z>([^<]+)</Z>', text)
                if mx and mz:
                    x = float(mx.group(1))
                    z = float(mz.group(1))
                    if -95 <= x <= -60 and -155 <= z <= -125:
                        m_name = re.search(r'<string name="Name">([^<]+)</string>', text)
                        m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', text)
                        m_mat = re.search(r'<token name="Material">([^<]+)</token>', text)
                        m_tex = re.findall(r'<Content name="Texture"><url>([^<]+)</url></Content>', text)
                        print(f"Part at ({x:6.1f}, {z:6.1f}): name={m_name.group(1):<30} mat={m_mat.group(1):<5} col={m_col.group(1):<10} tex={m_tex}")

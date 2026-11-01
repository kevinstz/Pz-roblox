rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# OX = 8102.5, OY = 11672.5
# x in [8097, 8103] -> cx in [(8097 + 0.5 - 8102.5)*3, (8103 + 0.5 - 8102.5)*3] = [-15.0, +3.0]
# y in [11678, 11685] -> cz in [(11678 + 0.5 - 11672.5)*3, (11685 + 0.5 - 11672.5)*3] = [18.0, 39.0]

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
                if 'Name">Suelo|' in text:
                    mx = re.search(r'<X>([^<]+)</X>', text)
                    mz = re.search(r'<Z>([^<]+)</Z>', text)
                    if mx and mz:
                        x = float(mx.group(1))
                        z = float(mz.group(1))
                        if -18 <= x <= 6 and 15 <= z <= 42:
                            m_name = re.search(r'<string name="Name">([^<]+)</string>', text)
                            m_size = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                            m_tex = re.findall(r'<Content name="Texture"><url>([^<]+)</url></Content>', text)
                            print(f"Suelo at ({x:5.1f}, {z:5.1f}): size=({m_size.group(1)}, {m_size.group(3)}) name={m_name.group(1)} num_tex={len(m_tex)}")

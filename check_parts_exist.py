import re

# What are the PZ coordinates of Rosewood center park and street?
# Park is around: x=8080..8110, y=11660..11680 (in PZ coordinates)
# Let's map PZ coordinates to Roblox world coordinates:
# OX = (8040 + 8165) / 2.0 = 8102.5
# OY = (11585 + 11760) / 2.0 = 11672.5
# TILE = 3.0
# cx = (x + w/2 - 8102.5) * 3
# cz = (y + h/2 - 11672.5) * 3

# For PZ x = 8080..8110: cx = (8080 - 8102.5)*3 = -67.5 to (+7.5)*3 = +22.5
# For PZ y = 11650..11690: cz = (11650 - 11672.5)*3 = -67.5 to (+17.5)*3 = +52.5

# Let's find all parts in PZ_Rosewood.rbxlx (current file) in Suelo_Piso_0
# in this coordinate box: X in [-100, 50], Z in [-100, 50]
p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

found_parts = []
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo = False
    in_part = False
    buf = []
    
    for line in f:
        if '<Item class="Model" referent="R739">' in line:
            in_suelo = True
            continue
        if in_suelo:
            if '<Item class="Part"' in line:
                in_part = True
                buf = [line]
                continue
            if in_part:
                buf.append(line)
                if '</Item>' in line and line.strip() == '</Item>':
                    # part closed
                    txt = "".join(buf)
                    in_part = False
                    buf = []
                    # check CFrame
                    m_x = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Z>([^<]+)</Z>', txt, re.DOTALL)
                    if m_x:
                        cx = float(m_x.group(1))
                        cz = float(m_x.group(2))
                        if -80 <= cx <= 40 and -80 <= cz <= 40:
                            m_name = re.search(r'<string name="Name">([^<]+)</string>', txt)
                            name = m_name.group(1) if m_name else "Unknown"
                            found_parts.append((cx, cz, name))
            if '<Item class="Model"' in line and 'R739' not in line:
                break

print(f"Total parts found in X[-80, 40], Z[-80, 40]: {len(found_parts)}")
for p in found_parts[:20]:
    print(f"  Part at ({p[0]:6.1f}, {p[1]:6.1f}): {p[2]}")

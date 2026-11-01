import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_terr = False
    lines = []
    for line in f:
        if 'name="Name">TerrenoCircundante' in line:
            in_terr = True
        if in_terr:
            lines.append(line)
            if '</Item>' in line and line.strip() == '</Item>':
                break

print("".join(lines[:60]))

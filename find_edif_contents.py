p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_edif = False
    lines = []
    for line in f:
        if 'name="Name">Edificios<' in line:
            in_edif = True
        if in_edif:
            lines.append(line)
            if len(lines) > 50:
                break

print("".join(lines))

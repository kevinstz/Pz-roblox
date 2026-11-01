p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_edif = False
    models = []
    for line in f:
        if 'name="Name">Edificios<' in line:
            in_edif = True
        if in_edif:
            if 'name="Name">' in line and 'Edificios' not in line:
                models.append(line.strip())
                if len(models) >= 20:
                    break

for m in models:
    print(m)

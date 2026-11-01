import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_edif = False
    depth = 0
    models = []
    for line in f:
        if '<string name="Name">Edificios</string>' in line:
            in_edif = True
            depth = 1
            continue
        if in_edif:
            if '<Item' in line:
                depth += 1
                if depth == 2 and 'class="Model"' in line:
                    models.append([line.strip()])
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    break
            elif depth == 2 and models:
                if 'name="Name"' in line:
                    models[-1].append(line.strip())

print(f"Total direct models inside Edificios: {len(models)}")
for m in models[:30]:
    print(" -> ".join(m))

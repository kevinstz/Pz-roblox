rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_ext = False
    models = []
    depth = 0
    for line in f:
        if 'name="Name">Exterior<' in line:
            in_ext = True
            depth = 1
            continue
        if in_ext:
            if '<Item' in line:
                depth += 1
                if depth == 2:
                    models.append([line.strip()])
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    break
            elif depth == 2 and models:
                if '<string name="Name">' in line:
                    models[-1].append(line.split('>')[1].split('<')[0])

print(f"Total folders/models inside Exterior: {len(models)}")
for m in models:
    print(m)

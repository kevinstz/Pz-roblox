rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_edif = False
    count = 0
    for idx, line in enumerate(f):
        if 'Name">Edificios<' in line:
            in_edif = True
            print(f"Edificios starts around line {idx}")
        if in_edif:
            if '<Item class="Model"' in line:
                count += 1
                if count <= 15:
                    print(f"  Model {count}: line {idx}")
            if '<string name="Name">' in line and count <= 15:
                print(f"    Name: {line.strip()}")
            if count > 15:
                break

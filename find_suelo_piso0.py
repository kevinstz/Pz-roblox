rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'Name">Suelo_Piso_0<' in line:
            print(f"Suelo_Piso_0 starts around L{i}")
        elif 'Name">Suelo_Piso_1<' in line:
            print(f"Suelo_Piso_1 starts around L{i}")
        elif 'Name">Suelo_Piso_2<' in line:
            print(f"Suelo_Piso_2 starts around L{i}")
        elif 'Name">Edificios<' in line:
            print(f"Edificios starts around L{i}")
            break

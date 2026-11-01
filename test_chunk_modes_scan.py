src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

in_suelo0 = False
chunk_modes = 0

with open(src, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'name="Name">Suelo_Piso_0<' in line:
            in_suelo0 = True
            print(f"Line {i}: Found Suelo_Piso_0 start")
            continue
        elif in_suelo0 and 'name="Name">Suelo_Piso_1<' in line:
            in_suelo0 = False
            print(f"Line {i}: Found Suelo_Piso_1 (end of Suelo_Piso_0)")
            break
        if in_suelo0 and '<token name="ModelStreamingMode">0</token>' in line:
            chunk_modes += 1

print("Total ModelStreamingMode tokens in Suelo_Piso_0:", chunk_modes)

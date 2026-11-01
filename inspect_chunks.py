rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    chunk_names = []
    in_suelo0 = False
    for line in f:
        if 'Suelo_Piso_0' in line:
            in_suelo0 = True
        if in_suelo0:
            if '<string name="Name">Chunk_' in line:
                chunk_names.append(line.strip())
            if '</Item>' in line and len(chunk_names) > 0 and 'Suelo_Piso_0' in line:
                break
    print(f"Total Chunk models found: {len(chunk_names)}")
    if chunk_names:
        print("Sample chunks:", chunk_names[:5])

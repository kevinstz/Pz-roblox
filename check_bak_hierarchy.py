BAK_RBXLX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_ground"

with open(BAK_RBXLX, 'r', encoding='utf-8', errors='ignore') as f:
    for idx in range(1, 2357377):
        line = f.readline()
        if idx >= 2357350:
            print(f"Line {idx}: {line[:80].rstrip()}")

BAK_RBXLX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_ground"

with open(BAK_RBXLX, 'r', encoding='utf-8', errors='ignore') as f:
    for i in range(1, 50600):
        line = f.readline()
        if i >= 50490:
            print(f"Line {i}: {line[:80].rstrip()}")

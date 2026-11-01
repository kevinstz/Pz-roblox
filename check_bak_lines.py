BAK_RBXLX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_ground"

with open(BAK_RBXLX, 'r', encoding='utf-8', errors='ignore') as f:
    for idx in range(1, 50445):
        line = f.readline()
        if idx >= 50430:
            print(f"Line {idx}: {line.strip()[:80]}")

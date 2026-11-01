p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    for idx in range(1, 1999395):
        line = f.readline()
        if idx >= 1999380:
            print(f"Line {idx}: {line[:80].rstrip()}")

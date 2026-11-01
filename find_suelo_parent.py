p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    for i in range(1, 260):
        line = f.readline()
        if i >= 200:
            print(f"Line {i}: {line.strip()[:80]}")

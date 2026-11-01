with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'Suelo_Piso_' in line:
            print(f"Line {idx+1}: {line.strip()}")

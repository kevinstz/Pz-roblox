with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        line_no = idx + 1
        if 2777430 <= line_no <= 2777455:
            print(f"{line_no}: {line.rstrip()}")
        if line_no > 2777455:
            break

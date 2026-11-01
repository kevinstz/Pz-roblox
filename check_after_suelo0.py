with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        line_no = idx + 1
        if 2777450 <= line_no <= 2777465:
            print(f"{line_no}: {line.strip()}")
        if line_no > 2777465:
            break

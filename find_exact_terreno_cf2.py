p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f, 1):
        if 9701920 <= idx <= 9701929:
            print(f"{idx}: {line[:80].rstrip()}")
        if idx > 9701929:
            break

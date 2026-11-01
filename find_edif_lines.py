rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'referent="R39347"' in line:
            print(f"Edificios start: line {i}")
        if 'referent="R116275"' in line:
            print(f"Exterior start (Edificios end): line {i}")
            break

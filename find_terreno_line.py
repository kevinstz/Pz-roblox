rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if 'TerrenoCircundante' in line:
            print(f"TerrenoCircundante at line {idx+1}")
            break

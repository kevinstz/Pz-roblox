rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'IsometricController' in line or 'SurvivorHUD' in line:
            print(f"Script at line {i+1}: {line.strip()[:100]}")

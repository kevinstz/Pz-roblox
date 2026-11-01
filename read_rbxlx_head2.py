rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i in range(250):
        line = f.readline()
        if i >= 120:
            print(f"{i+1:3d}: {line.strip()[:100]}")

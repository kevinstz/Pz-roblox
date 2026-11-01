src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(src, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 2047260 <= i <= 2047276:
            print(f"{i}: {line}", end="")

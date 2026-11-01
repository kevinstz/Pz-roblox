rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    for idx, line in enumerate(f):
        if idx >= 9664870:
            print(f"{idx}: {line.rstrip()}")
            if idx >= 9665110:
                break

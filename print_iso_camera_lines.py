rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    for idx, line in enumerate(f):
        if 9664700 <= idx <= 9664900:
            print(f"{idx}: {line.rstrip()}")

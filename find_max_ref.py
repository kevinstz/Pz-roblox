import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
max_r = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m = re.findall(r'referent="R(\d+)"', line)
        for r in m:
            val = int(r)
            if val > max_r:
                max_r = val

print("Max referent R:", max_r)

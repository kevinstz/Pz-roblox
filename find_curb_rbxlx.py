rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
target = 'street_curbs_01_11'
found = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if target in line or '969234b5beed7cdc6e68' in line:
            print(f"L{i}: {line.strip()[:100]}")
            found += 1
            if found >= 10:
                break
print(f"Total found: {found}")

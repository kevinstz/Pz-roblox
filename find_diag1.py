rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
found = False
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'street_curbs_01_diag' in line:
            print(f"L{i}: {line.strip()[:100]}")
            found = True
            break
if not found:
    print("NOT FOUND AT ALL in PZ_Rosewood.rbxlx!")


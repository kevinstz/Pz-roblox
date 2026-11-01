rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    cap = False
    for line in f:
        if 'referent="R17077"' in line:
            cap = True
        if cap:
            lines.append(line)
            if len(lines) > 20:
                break
    print("".join(lines))

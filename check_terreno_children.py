rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    buf = []
    cap = False
    for line in f:
        if 'Name">TerrenoCircundante' in line:
            cap = True
        if cap:
            buf.append(line)
            if '</Item>' in line:
                print("".join(buf))
                break

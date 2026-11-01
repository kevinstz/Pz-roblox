rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    capture = False
    for line in f:
        if '<Item class="Model"' in line:
            lines = [line]
            capture = True
            continue
        if capture:
            lines.append(line)
            if 'Suelo_Piso_0' in line:
                print("".join(lines[:30]))
                break
            if len(lines) > 50:
                capture = False
                lines = []

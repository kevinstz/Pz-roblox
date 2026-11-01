rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    capturing = False
    lines = []
    for line in f:
        if '<Item class="Texture"' in line or '<Item class="Decal"' in line:
            capturing = True
        if capturing:
            lines.append(line)
            if '</Item>' in line:
                break

print("".join(lines))

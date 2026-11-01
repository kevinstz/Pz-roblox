rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'name="Name">Office_31_45_24<' in line:
            start = i
            break

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    capture = False
    for i, line in enumerate(f):
        if i >= start:
            if '<Item class="Part"' in line:
                capture = True
            if capture:
                lines.append(line)
                if '</Item>' in line:
                    print("".join(lines[:45]))
                    break

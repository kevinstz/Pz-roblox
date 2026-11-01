p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_model = False
    lines = []
    for line in f:
        if '<Item class="Model" referent="R739">' in line:
            in_model = True
        if in_model:
            lines.append(line)
            if '<Item' in line and 'referent="R739"' not in line:
                break

print("".join(lines))

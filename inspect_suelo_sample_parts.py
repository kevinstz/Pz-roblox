p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo = False
    part_lines = []
    part_count = 0
    for line in f:
        if '<Item class="Model" referent="R739">' in line:
            in_suelo = True
            continue
        if in_suelo:
            if '<Item class="Part"' in line:
                part_count += 1
                if part_count <= 3:
                    part_lines.append(line)
            elif part_count <= 3:
                part_lines.append(line)
                if '</Item>' in line and part_lines.count('</Item>') == part_count:
                    if part_count == 3:
                        break

print("".join(part_lines[:80]))

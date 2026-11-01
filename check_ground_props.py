p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo = False
    suelo_lines = []
    in_terr = False
    terr_lines = []
    for line in f:
        if 'name="Name">TerrenoCircundante<' in line:
            in_terr = True
        if in_terr:
            terr_lines.append(line)
            if '</Properties>' in line or '</Item>' in line:
                in_terr = False
        if 'name="Name">Suelo_Piso_0<' in line:
            in_suelo = True
        if in_suelo:
            suelo_lines.append(line)
            if '</Properties>' in line:
                in_suelo = False
                break

print("=== TerrenoCircundante ===")
print("".join(terr_lines[:25]))
print("=== Suelo_Piso_0 ===")
print("".join(suelo_lines[:25]))

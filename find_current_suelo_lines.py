p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    start_line = None
    end_line = None
    depth = 0
    in_suelo = False
    
    for idx, line in enumerate(f, 1):
        if 'name="Name">Suelo_Piso_0<' in line:
            # find where the Item opened
            pass
        if '<Item class="Model" referent="R739">' in line or '<Item class="Folder" referent="R739">' in line:
            start_line = idx
            in_suelo = True
            depth = 1
            continue
        if in_suelo:
            if '<Item' in line:
                depth += 1
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    end_line = idx
                    break

print(f"Current Suelo_Piso_0 starts at line {start_line} and ends at line {end_line}")
print(f"Total lines in Suelo_Piso_0: {end_line - start_line + 1}")

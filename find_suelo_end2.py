with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    target_start = 50439 # where <Item class="Model" referent="R739"> is
    depth = 0
    for idx, line in enumerate(f):
        line_no = idx + 1
        if line_no < 50435:
            continue
        if '<Item' in line:
            depth += 1
            if line_no == 50439:
                print(f"Start of Suelo_Piso_0 at line {line_no}")
        if '</Item>' in line:
            depth -= 1
            if depth == 0 and line_no > 50439:
                print(f"End of Suelo_Piso_0 at line {line_no}")
                break
            if line_no % 500000 == 0:
                print(f"Scanned line {line_no}, current depth = {depth}")

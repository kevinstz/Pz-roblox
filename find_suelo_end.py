with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    in_suelo0 = False
    depth = 0
    start_line = 0
    for idx, line in enumerate(f):
        if 'Suelo_Piso_0' in line:
            in_suelo0 = True
            start_line = idx + 1
            print(f"Found Suelo_Piso_0 at line {start_line}")
        if in_suelo0:
            if '<Item' in line:
                depth += 1
            if '</Item>' in line:
                depth -= 1
                if depth == 0:
                    print(f"Suelo_Piso_0 ends at line {idx+1}")
                    # read next 10 lines
                    for _ in range(10):
                        print(f.readline().strip())
                    break

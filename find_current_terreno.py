p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_item = False
    buf = []
    for line in f:
        if '<Item class="Part"' in line:
            in_item = True
            buf = [line]
            continue
        if in_item:
            buf.append(line)
            if 'name="Name">TerrenoCircundante' in line:
                for b in buf:
                    if '<X>' in b or '<Y>' in b or '<Z>' in b or 'CFrame' in b:
                        print(b.strip())
                break
            if '</Item>' in line and line.strip() == '</Item>':
                in_item = False
                buf = []

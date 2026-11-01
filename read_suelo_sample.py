with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    buf = []
    cap = False
    for line in f:
        if '<Item class="Part"' in line:
            cap = True
            buf = [line]
            continue
        if cap:
            buf.append(line)
            if '</Item>' in line and 'Suelo|' in ''.join(buf):
                print(''.join(buf[:40]))
                # print all of it
                print(''.join(buf))
                break

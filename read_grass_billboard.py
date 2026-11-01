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
            if '</Item>' in line:
                cap = False
                text = ''.join(buf)
                if 'blends_grassoverlays_01_' in text and '8.5732' in text:
                    print(text[:1500])
                    break

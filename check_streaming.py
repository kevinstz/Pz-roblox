p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_ws = False
    for line in f:
        if '<Item class="Workspace"' in line:
            in_ws = True
        if in_ws:
            if 'Streaming' in line or 'Stream' in line:
                print(line.strip())
            if '</Properties>' in line:
                break

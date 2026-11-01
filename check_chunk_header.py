p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    buf = []
    for line in f:
        buf.append(line)
        if len(buf) > 40:
            buf.pop(0)
        if '<string name="Name">Chunk_0_0</string>' in line:
            for b in buf:
                print(b.rstrip())
            break

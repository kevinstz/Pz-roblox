p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    chunk_lines = []
    in_chunk = False
    for line in f:
        if '<string name="Name">Chunk_' in line:
            in_chunk = True
        if in_chunk:
            chunk_lines.append(line)
            if '<Item class="Part"' in line:
                break

print("".join(chunk_lines))

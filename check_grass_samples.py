import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

grass_samples = []
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    in_grass = False
    buf = []
    for line in f:
        if '<Item class="Part"' in line:
            in_grass = True
            buf = [line]
            continue
        if in_grass:
            buf.append(line)
            if 'blends_grassoverlays_01_' in line:
                pass
            if '</Item>' in line and line.strip() == '</Item>':
                txt = "".join(buf)
                if 'blends_grassoverlays_01_' in txt:
                    grass_samples.append(txt)
                    if len(grass_samples) >= 3:
                        break
                in_grass = False
                buf = []

print(f"Sample grass parts found: {len(grass_samples)}")
for g in grass_samples:
    print(g[:600])
    print("="*40)

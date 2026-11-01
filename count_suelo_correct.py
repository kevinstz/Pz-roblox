rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

total_suelo = 0
suelo_multi_tex = 0
max_tex = 0

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_suelo = False
    cur_tex_count = 0
    for line in f:
        if '<Item class="Part"' in line:
            in_suelo = False
            cur_tex_count = 0
        elif 'Name">Suelo|' in line:
            in_suelo = True
            total_suelo += 1
        elif in_suelo:
            if '<Item class="Texture"' in line:
                cur_tex_count += 1
            elif '</Item>' in line and cur_tex_count > 0:
                # Could be closing texture or closing part
                pass
            if cur_tex_count > 1:
                suelo_multi_tex += 1
                max_tex = max(max_tex, cur_tex_count)
                in_suelo = False

print(f"Total Suelo parts: {total_suelo}")
print(f"Suelo parts with >1 Texture: {suelo_multi_tex}")
print(f"Max textures on a single Suelo part: {max_tex}")

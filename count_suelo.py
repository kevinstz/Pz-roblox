rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

total_suelo = 0
suelo_multi_tex = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    cap = False
    for line in f:
        if '<Item class="Part"' in line:
            cap = True
            lines = [line]
            continue
        if cap:
            lines.append(line)
            if '</Item>' in line:
                cap = False
                text = "".join(lines)
                if 'Name">Suelo|' in text:
                    total_suelo += 1
                    n_tex = len(re.findall(r'<Item class="Texture"', text))
                    if n_tex > 1:
                        suelo_multi_tex += 1

print(f"Total Suelo parts: {total_suelo}")
print(f"Suelo parts with >1 Texture: {suelo_multi_tex}")

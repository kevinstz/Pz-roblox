import os

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    capturing = False
    lines = []
    found = 0
    for line in f:
        if '<Item class="Part"' in line:
            capturing = True
            lines = [line]
            continue
        if capturing:
            lines.append(line)
            if '</Item>' in line:
                capturing = False
                text = ''.join(lines)
                if 'blends_street_01_48' in text or 'blends_natural_01_64' in text or 'street_curbs' in text:
                    print(text[:1500])
                    print('...' if len(text) > 1500 else '')
                    print('=' * 50)
                    found += 1
                    if found >= 3:
                        break

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
# x = 8112 -> cx = (8112 + 0.5 - 8102.5) * 3 = 10.0 * 3 = 30.0 (or 28.5)
# y = 11629 -> cz = (11629 + 0.5 - 11672.5) * 3 = -43.0 * 3 = -129.0 (or -130.5)

import re

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
                    mx = re.search(r'<X>([^<]+)</X>', text)
                    mz = re.search(r'<Z>([^<]+)</Z>', text)
                    if mx and mz:
                        x = float(mx.group(1))
                        z = float(mz.group(1))
                        if 24 <= x <= 36 and -135 <= z <= -125:
                            print(f"Suelo at ({x:.1f}, {z:.1f}):\n{text[:1200]}")
                            # find all Texture items inside this Part
                            texs = re.findall(r'<Item class="Texture"[^>]*>.*?</Item>', text, re.DOTALL)
                            print(f"Found {len(texs)} Texture children:")
                            for t in texs:
                                t_url = re.search(r'<url>([^<]+)</url>', t)
                                t_zi = re.search(r'<int name="ZIndex">([^<]+)</int>', t)
                                print(f"  Texture url={t_url.group(1) if t_url else ''}, zindex={t_zi.group(1) if t_zi else ''}")
                            print("=" * 60)

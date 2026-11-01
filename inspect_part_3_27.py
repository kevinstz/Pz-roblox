rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
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
                        if abs(x - (-3.0)) < 0.1 and abs(z - 27.0) < 0.1:
                            print(f"Exact Part at ({x}, {z}):\n{text}")
                            break

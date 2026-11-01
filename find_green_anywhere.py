rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    cap = False
    green_parts = []
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
                m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', text)
                if m_col:
                    col = int(m_col.group(1))
                    r = (col >> 16) & 0xFF
                    g = (col >> 8) & 0xFF
                    b = col & 0xFF
                    if g > 70 and g > r + 20 and g > b + 10: # green
                        m_name = re.search(r'<string name="Name">([^<]+)</string>', text)
                        mx = re.search(r'<X>([^<]+)</X>', text)
                        mz = re.search(r'<Z>([^<]+)</Z>', text)
                        name = m_name.group(1) if m_name else ''
                        x = float(mx.group(1)) if mx else 0
                        z = float(mz.group(1)) if mz else 0
                        green_parts.append((name, col, (r, g, b), x, z))
                        if len(green_parts) >= 20:
                            break

print(f"Total green parts found (sample): {len(green_parts)}")
for p in green_parts[:15]:
    print(p)

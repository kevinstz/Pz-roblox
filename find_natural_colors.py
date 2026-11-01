rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    lines = []
    cap = False
    natural_parts = []
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
                if 'Name">Suelo|blends_natural' in text or 'Name">Suelo|floors_exterior_natural' in text:
                    m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', text)
                    m_name = re.search(r'<string name="Name">([^<]+)</string>', text)
                    if m_col and m_name:
                        col = int(m_col.group(1))
                        r = (col >> 16) & 0xFF
                        g = (col >> 8) & 0xFF
                        b = col & 0xFF
                        natural_parts.append((m_name.group(1), col, (r, g, b)))
                        if len(natural_parts) >= 15:
                            break

print(f"Sample natural floor parts ({len(natural_parts)}):")
for p in natural_parts:
    print(p)

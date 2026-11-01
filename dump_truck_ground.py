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
                        if -88 <= x <= -70 and -145 <= z <= -130:
                            m_name = re.search(r'<string name="Name">([^<]+)</string>', text)
                            m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', text)
                            m_mat = re.search(r'<token name="Material">([^<]+)</token>', text)
                            m_size = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                            m_tex = re.findall(r'<Content name="Texture"><url>([^<]+)</url></Content>', text)
                            print(f"Suelo at ({x:5.1f}, {z:5.1f}): size=({m_size.group(1)}, {m_size.group(3)}) name={m_name.group(1)} col={m_col.group(1)} tex={m_tex}")

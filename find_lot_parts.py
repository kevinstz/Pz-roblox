rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

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
                    # check CFrame
                    # <X>...</X>
                    # <Z>...</Z>
                    import re
                    mx = re.search(r'<X>([^<]+)</X>', text)
                    mz = re.search(r'<Z>([^<]+)</Z>', text)
                    if mx and mz:
                        x = float(mx.group(1))
                        z = float(mz.group(1))
                        if -160 <= x <= -120 and 120 <= z <= 150:
                            m_name = re.search(r'<string name="Name">([^<]+)</string>', text)
                            m_tex = re.findall(r'<Content name="Texture"><url>([^<]+)</url></Content>', text)
                            m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', text)
                            print(f"Part at ({x:.1f}, {z:.1f}): name={m_name.group(1) if m_name else ''}, color={m_col.group(1) if m_col else ''}, tex={m_tex}")

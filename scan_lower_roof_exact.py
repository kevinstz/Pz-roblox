with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

# Find all parts with pos near X in [-55, -45], Y in [6, 12], Z in [-75, -60]
for m in re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    block = m.group(0)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    if m_cf:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        if -55 <= x <= -44 and 5.5 <= y <= 13.0 and -75 <= z <= -58:
            m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
            name = m_name.group(1) if m_name else "?"
            cls = m.group(1)
            # check if decal exists
            m_dec = re.search(r'<url>([^<]+)</url>', block)
            dec = m_dec.group(1) if m_dec else "none"
            m_tr = re.search(r'<float name="Transparency">([^<]+)</float>', block)
            tr = m_tr.group(1) if m_tr else "0"
            m_s = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
            sz = f"({float(m_s.group(1)):.2f}, {float(m_s.group(2)):.2f}, {float(m_s.group(3)):.2f})" if m_s else "?"
            print(f"Ref={m.group(2)} | Cls={cls:12s} | Name={name:30s} | Pos=({x:6.2f}, {y:5.2f}, {z:6.2f}) | Sz={sz} | Tr={tr} | Dec={dec}")

with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

for m in re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    block = m.group(0)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    name = m_name.group(1) if m_name else ""
    if 'walls_exterior_roofs' in name:
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if -60 <= x <= -40 and -80 <= z <= -60:
                m_dec = re.search(r'<url>([^<]+)</url>', block)
                dec = m_dec.group(1) if m_dec else "none"
                m_tr = re.search(r'<float name="Transparency">([^<]+)</float>', block)
                tr = m_tr.group(1) if m_tr else "0"
                print(f"Ref={m.group(2)} | Name={name:30s} | Pos=({x:.2f}, {y:.2f}, {z:.2f}) | Tr={tr} | Dec={dec}")

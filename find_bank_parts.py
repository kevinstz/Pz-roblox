with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<string name="Name">location_business_bank_01_', text)]
print(f"Total location_business_bank_01 parts: {len(matches)}")
for idx in matches:
    part_idx = text.rfind('<Item class="Part"', 0, idx)
    end_idx = text.find('</Item>', idx)
    block = text[part_idx:end_idx+7]
    m_ref = re.search(r'referent="([^"]+)"', block)
    ref = m_ref.group(1) if m_ref else "?"
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    name = m_name.group(1) if m_name else "?"
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else "?"
    print(f"Ref={ref} | Name={name} | Pos={pos}")

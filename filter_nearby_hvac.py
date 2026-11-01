import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

hvac_parts = []
for m in re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    if m_name and ('rooftop' in m_name.group(1) or 'vent' in m_name.group(1) or 'furniture_roof' in m_name.group(1)):
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if -70 <= x <= 10 and -100 <= z <= 10:
                hvac_parts.append((ref, m_name.group(1), x, y, z))

print(f"Nearby rooftop parts: {len(hvac_parts)}")
for p in hvac_parts:
    print(f"HVAC: Ref={p[0]} | Name={p[1]} | Pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f})")

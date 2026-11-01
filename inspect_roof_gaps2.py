import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('<string name="Name">Exterior_8080_11648</string>')
item_start = text.rfind('<Item class="Model"', 0, idx)
next_model = text.find('\n\t\t\t\t<Item class="Model"', idx)
chunk = text[item_start:next_model]

matches = list(re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', chunk, re.DOTALL))
print(f"Parts in Exterior_8080_11648: {len(matches)}")

count = 0
for m in matches:
    b = m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', b)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', b, re.DOTALL)
    m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', b, re.DOTALL)
    if m_cf and m_sz and m_name and 'roof' in m_name.group(1).lower():
        print(f"Name={m_name.group(1):24s} | Pos=({float(m_cf.group(1)):6.2f}, {float(m_cf.group(2)):6.2f}, {float(m_cf.group(3)):6.2f}) | Size=({float(m_sz.group(1)):.4f}, {float(m_sz.group(2)):.4f}, {float(m_sz.group(3)):.4f})")
        count += 1
        if count >= 15: break

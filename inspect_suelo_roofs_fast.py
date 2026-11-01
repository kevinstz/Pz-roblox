import re

with open(r"out\PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

target = '<string name="Name">Suelo|roofs_03_54</string>'
pos = 0
found = 0
xs, ys, zs = [], [], []

while True:
    idx = text.find(target, pos)
    if idx == -1:
        break
    found += 1
    # find enclosing item
    item_start = text.rfind('<Item class="', max(0, idx - 4000), idx)
    item_end = text.find('</Item>', idx)
    block = text[item_start:item_end]
    
    # parse cframe
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block, re.DOTALL)
    m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', block)
    m_tex = re.search(r'<url>([^<]+)</url>', block)
    
    if m_cf:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        xs.append(x)
        ys.append(y)
        zs.append(z)
        if found <= 5:
            print(f"[{found}] Pos: ({x:.2f}, {y:.2f}, {z:.2f}), Size: {m_sz.groups() if m_sz else '?'}, Tex: {m_tex.group(1) if m_tex else '?'}")
    pos = idx + len(target)

print(f"Total found: {found}")
if xs:
    print(f"Bounds: X=[{min(xs):.1f}, {max(xs):.1f}], Y=[{min(ys):.1f}, {max(ys):.1f}], Z=[{min(zs):.1f}, {max(zs):.1f}]")

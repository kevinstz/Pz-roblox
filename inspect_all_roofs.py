import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search all parts with 'roofs_' or 'roof'
# And check their size, texture, and why they might have 'recuadros partidos'
matches = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
roofs = []
for m in matches:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    if m_name and ('roof' in m_name.group(1).lower() or 'techo' in m_name.group(1).lower()):
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        m_tex = re.findall(r'<url>([^<]+)</url>', block)
        m_tex_cls = re.findall(r'<Item class="([^"]+)"', block)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            roofs.append({
                'ref': ref, 'cls': cls, 'name': m_name.group(1),
                'pos': (x, y, z), 'sz': sz, 'tex': m_tex, 'children': m_tex_cls
            })

print(f"Total roof parts: {len(roofs)}")

# Sample roofs from houses (X > 100):
house_roofs = [r for r in roofs if r['pos'][0] > 100]
print(f"House roofs (X > 100): {len(house_roofs)}")
for r in house_roofs[:20]:
    print(f"Ref={r['ref']:8s} | Cls={r['cls']:10s} | Name={r['name']:30s} | Pos=({r['pos'][0]:6.1f}, {r['pos'][1]:6.1f}, {r['pos'][2]:6.1f}) | Size={r['sz']} | Children={r['children']}")

# Sample roofs from downtown (X < 0):
dt_roofs = [r for r in roofs if r['pos'][0] < 0]
print(f"Downtown roofs (X < 0): {len(dt_roofs)}")
for r in dt_roofs[:20]:
    print(f"Ref={r['ref']:8s} | Cls={r['cls']:10s} | Name={r['name']:30s} | Pos=({r['pos'][0]:6.1f}, {r['pos'][1]:6.1f}, {r['pos'][2]:6.1f}) | Size={r['sz']} | Children={r['children']}")

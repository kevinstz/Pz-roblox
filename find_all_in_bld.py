# Let's find all parts around X in [-60, -30], Z in [-80, -20], Y in [0, 25]
import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all parts and their names, positions, colors, meshes, decals
# Using regex iterating over <Item class="Part" or <Item class="MeshPart"
items = re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)

found_corner = []
for m in items:
    cls, ref, block = m.group(1), m.group(2), m.group(3)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    if m_cf and m_name:
        x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
        # near the building in r1c0 and r2c0:
        if -55 <= x <= -40 and -75 <= z <= -25 and 0 <= y <= 25:
            m_col = re.search(r'<Color3uint8 name="Color3uint8">([^<]+)</Color3uint8>', block)
            m_sz = re.search(r'<Vector3 name="size">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
            m_tex = re.findall(r'<url>([^<]+)</url>', block)
            sz = (float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))) if m_sz else ()
            found_corner.append({
                'cls': cls, 'ref': ref, 'name': m_name.group(1),
                'pos': (x, y, z), 'col': m_col.group(1) if m_col else '',
                'size': sz, 'tex': m_tex
            })

print(f"Total parts in building region: {len(found_corner)}")

# Let's see all parts with white or light color or without texture or special names
for p in found_corner:
    # Check if white/light or mesh or street_decoration or arch or door or roof
    print(f"Ref={p['ref']:8s} | Cls={p['cls']:8s} | Name={p['name']:32s} | Pos=({p['pos'][0]:6.2f}, {p['pos'][1]:6.2f}, {p['pos'][2]:6.2f}) | Size={p['size']} | Col={p['col']} | Tex={p['tex']}")

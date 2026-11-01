# Let's find every part of the wall in v4_tile_r1_c0.jpg and v4_tile_r2_c0.jpg
# That wall runs along the roof edge of Bar_31_45_12 / Exterior_8080_11648
# Let's project its coordinates and list all parts along it
import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all parts in Exterior_8080_11648 or Bar_31_45_12 around that wall
# The wall in v4_tile_r1_c0.jpg has a parapet coping (stone on top)
# Coping is walls_detailing_01_5 at Y = 22.46 or Y = 15.09 or Y = 7.74?
# Wait! At what Y is the coping in v4_tile_r1_c0.jpg?
coping_parts = []
for m in re.finditer(r'<Item class="Part" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    ref, block = m.group(1), m.group(2)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    if m_name and 'walls_detailing_01_' in m_name.group(1):
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            if -60 <= x <= -35 and -80 <= z <= -20:
                coping_parts.append((ref, m_name.group(1), x, y, z))

print(f"Coping parts near building: {len(coping_parts)}")
# group by Y
from collections import defaultdict
by_y = defaultdict(list)
for p in coping_parts:
    by_y[round(p[3], 1)].append(p)

for y, lst in sorted(by_y.items()):
    print(f"Y={y}: {len(lst)} coping parts, X range=[{min(p[2] for p in lst):.1f}..{max(p[2] for p in lst):.1f}], Z range=[{min(p[4] for p in lst):.1f}..{max(p[4] for p in lst):.1f}]")

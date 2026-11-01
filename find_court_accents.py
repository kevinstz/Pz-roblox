# Find the exact part protruding under the window in crop_v4_court_windows.jpg
from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

# Let us search all parts in the place file (not just pair2 region) around this wall:
with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let us find parts in Exterior_8112_11632 or adjacent models:
for m in re.finditer(r'<Item class="([^"]+)" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL):
    block = m.group(0)
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    name = m_name.group(1) if m_name else ""
    # if it has "roofs_accents" or "accent" or "rafter" or "shallow"
    if 'roofs_accents' in name or 'roof' in name:
        m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
        if m_cf:
            x, y, z = float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))
            # If in the vicinity of Knox Bank / Court wall:
            if 30 <= x <= 75 and -95 <= z <= -70 and 5 <= y <= 20:
                print(f"Ref={m.group(2)} | Cls={m.group(1)} | Name={name:30s} | pos=({x:.2f}, {y:.2f}, {z:.2f})")

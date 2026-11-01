import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find tiles where both natural and street appear, or where natural borders street
transitions = []
for (x, y, z), names in squares.items():
    if z == 0:
        has_nat = any('natural' in n for n in names)
        has_str = any('street' in n for n in names)
        if has_nat and has_str:
            transitions.append((x, y, names))

print(f"Total tiles with both natural and street: {len(transitions)}")
print("Sample tiles (first 10):")
for t in transitions[:10]:
    print(t)

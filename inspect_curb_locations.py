import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find coordinates where street_curbs_01 appears
curb_locs = []
for (x, y, z), names in squares.items():
    for n in names:
        if 'street_curbs_01' in n:
            curb_locs.append((x, y, z, n, names))

print(f"Total curb occurrences: {len(curb_locs)}")
print("Sample curb occurrences (first 10):")
for c in curb_locs[:10]:
    print(c)

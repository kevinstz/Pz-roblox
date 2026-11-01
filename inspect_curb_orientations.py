import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os
from collections import defaultdict

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find coordinates of all curbs
by_name = defaultdict(list)
for (x, y, z), names in squares.items():
    for n in names:
        if n.startswith('street_curbs_01_'):
            by_name[n].append((x, y))

for n, pts in sorted(by_name.items()):
    # Check if pts extend more in x or more in y
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    dx = max(xs) - min(xs)
    dy = max(ys) - min(ys)
    print(f"{n:<20}: count={len(pts):4d}, spanX={dx:3d}, spanY={dy:3d}")

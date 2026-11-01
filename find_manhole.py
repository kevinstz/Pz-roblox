import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find manhole / sewer cover in squares
for (x, y, z), names in squares.items():
    for n in names:
        if 'manhole' in n.lower() or 'drain' in n.lower() or 'sewer' in n.lower() or 'street_decoration_01_15' in n:
            print(f"Manhole candidate at ({x}, {y}, {z}): {names}")

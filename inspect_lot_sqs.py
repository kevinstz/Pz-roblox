import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Check all tiles around (8050..8066, 11702..11720)
print(f"Parking lot squares:")
all_tile_names = set()
for y in range(11703, 11720):
    for x in range(8053, 8066):
        sq = squares.get((x, y, 0), [])
        for n in sq:
            all_tile_names.add(n)

print(f"All tile names in parking lot ({len(all_tile_names)} total):")
for n in sorted(all_tile_names):
    print(" ", n)

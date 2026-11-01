import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find all curbs and corner curbs around (8100..8120, 11620..11640)
for y in range(11618, 11640):
    for x in range(8105, 8122):
        sq = squares.get((x, y, 0), [])
        curbs = [s for s in sq if 'curb' in s or 'diag' in s or 'trafficlines' in s]
        if curbs:
            print(f"({x}, {y}): {curbs}")

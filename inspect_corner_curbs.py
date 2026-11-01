import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

print("Tiles around (8108, 11629):")
for y in range(11625, 11634):
    for x in range(8104, 8114):
        sq = squares.get((x, y, 0), [])
        if any('curb' in s for s in sq) or any('decoration' in s for s in sq):
            print(f"({x}, {y}): {sq}")

import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

for y in range(11627, 11632):
    print(f"\n--- y = {y} ---")
    for x in range(8107, 8116):
        sq = squares.get((x, y, 0), [])
        print(f"  x={x}: {sq}")

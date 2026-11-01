import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

print("Tiles at house front (8147..8153, 11684..11690):")
for y in range(11684, 11691):
    print(f"\n--- y = {y} ---")
    for x in range(8147, 8153):
        sq = squares.get((x, y, 0), [])
        print(f"  x={x}: {sq}")

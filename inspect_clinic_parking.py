import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

print("Tiles from (8070..8080, 11621..11632):")
for y in range(11621, 11631):
    row = []
    for x in range(8072, 8080):
        sq = squares.get((x, y, 0), [])
        base = sq[0] if sq else "None"
        row.append(f"{base:<25}")
    print(f"y={y}:")
    for r in row:
        print("  ", r)

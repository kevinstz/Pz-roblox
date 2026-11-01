import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find where parking lines are
parking_tiles = []
for (x, y, z), names in squares.items():
    for n in names:
        if 'parking' in n.lower() or 'traffic' in n.lower():
            parking_tiles.append((x, y, z, n))
            if len(parking_tiles) <= 15:
                print(f"Parking line at ({x}, {y}, {z}): {names}")
            break
print(f"Total parking line tiles: {len(parking_tiles)}")

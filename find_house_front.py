import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find coordinates where outdoor lamp + street bench are in front of house
for (x, y, z), names in squares.items():
    if z == 0:
        if any('lighting_outdoor' in n for n in names):
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    sq = squares.get((x+dx, y+dy, 0), [])
                    if any('bench' in s or 'furniture_seating' in s for s in sq):
                        print(f"House front match at ({x}, {y}): lamp={names}, nearby={sq}")
                        break

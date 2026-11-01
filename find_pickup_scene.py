import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find where potted plants or rubbish containers are next to exterior street
for (x, y, z), names in squares.items():
    if z == 0:
        for n in names:
            if 'vegetation_ornamental' in n or 'planter' in n or 'rubbish_containers' in n:
                # check if nearby tiles have street_trafficlines
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        sq = squares.get((x+dx, y+dy, 0), [])
                        if any('trafficlines' in s for s in sq):
                            print(f"Match at ({x}, {y}): obj={n}, nearby_tile={sq}")
                            break

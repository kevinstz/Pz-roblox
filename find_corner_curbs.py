import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Find coordinates where corner curbs appear
for (x, y, z), names in squares.items():
    for n in names:
        if n in ['street_curbs_01_0', 'street_curbs_01_1', 'street_curbs_01_2', 'street_curbs_01_3',
                 'street_curbs_01_4', 'street_curbs_01_5', 'street_curbs_01_6', 'street_curbs_01_7']:
            print(f"Corner curb {n} at ({x}, {y}): {names}")

import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

for y in range(11636, 11648):
    row = []
    for x in range(8040, 8052):
        sq = squares.get((x, y, 0), [])
        base = sq[0] if sq else "None"
        # shorten
        if 'street_01_' in base:
            idx = base.split('street_01_')[1]
            row.append(f"s{idx:<3}")
        elif 'natural_01_' in base:
            idx = base.split('natural_01_')[1]
            row.append(f"n{idx:<3}")
        else:
            row.append(base[:4])
    print(f"y={y}: " + " ".join(row))

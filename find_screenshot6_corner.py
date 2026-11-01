import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# In Screenshot 6, there is a manhole in the asphalt road, near a rounded curb corner.
# Earlier we found manholes at:
# (8042, 11605)
# (8046, 11675)
# (8066, 11626)
# (8104, 11595)
# (8108, 11629)
# (8104, 11683)
# (8104, 11685)
# (8104, 11743)
# (8136, 11657)
# (8136, 11691)
# (8144, 11597)
# (8147, 11632)

# Check which of these has a corner curb within 5 tiles:
for mx, my in [(8042, 11605), (8046, 11675), (8066, 11626), (8104, 11595), (8108, 11629),
               (8104, 11683), (8104, 11685), (8104, 11743), (8136, 11657), (8136, 11691), (8144, 11597), (8147, 11632)]:
    corners = []
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            sq = squares.get((mx+dx, my+dy, 0), [])
            for s in sq:
                if 'curb' in s:
                    corners.append((mx+dx, my+dy, s))
    if len(corners) > 0:
        print(f"Manhole at ({mx}, {my}): {len(corners)} nearby curb tiles:")
        for c in corners[:6]:
            print("  ", c)

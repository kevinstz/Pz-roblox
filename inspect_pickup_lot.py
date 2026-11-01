import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

for (v_type, vx, vy, vang) in [
    ('civilian', 8076, 11626, 0),
    ('wagon', 8083, 11626, 0),
    ('civilian', 8095, 11652, 90),
    ('wagon', 8095, 11660, 90),
]:
    print(f"\n--- {v_type} at ({vx}, {vy}) ---")
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            sq = squares.get((vx + dx, vy + dy, 0), [])
            print(f"({vx+dx}, {vy+dy}): {sq}")

import sys, os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

squares, rooms, headers = load_region(os.path.join(MEDIA, 'maps', 'Muldraugh, KY'), 8040, 11585, 8165, 11760)

for y in range(11680, 11688):
    for x in range(8078, 8086):
        sq = squares.get((x, y, 0), [])
        print(f"({x}, {y}): {sq}")

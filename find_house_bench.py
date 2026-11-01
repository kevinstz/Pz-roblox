# Let's find the house in media_1793236645437_2ff7f033.png
# It has porch with a bench, lamp post, door, two planters on porch.
# Planters: look like 'vegetation_ornamental_01' or similar, bench is 'furniture_seating_outdoor_01'
import sys, os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

squares, rooms, headers = load_region(os.path.join(MEDIA, 'maps', 'Muldraugh, KY'), 8040, 11585, 8165, 11760)

for (x, y, z), names in squares.items():
    if z == 0 and any('furniture_seating_outdoor' in n for n in names):
        print(f"Bench at ({x}, {y}): {names}")

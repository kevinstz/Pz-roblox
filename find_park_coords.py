import sys, os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

squares, rooms, headers = load_region(os.path.join(MEDIA, 'maps', 'Muldraugh, KY'), 8040, 11585, 8165, 11760)

# The park has brick border: 'floors_exterior_tilesandstone_01_3' or similar, or 'street_curbs'
for (x, y, z), names in squares.items():
    if z == 0 and any('brick' in n.lower() or 'red' in n.lower() for n in names):
        print(f"Red/brick at ({x}, {y}): {names}")
        break

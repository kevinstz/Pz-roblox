import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

MAPDIR = rf"{MEDIA}\maps\Muldraugh, KY"
squares, rooms, headers = load_region(MAPDIR, 8040, 11585, 8165, 11760)

total_squares = (8165 - 8040 + 1) * (11760 - 11585 + 1)
z0_squares = sum(1 for (x, y, z) in squares if z == 0)

print(f"Total grid squares in region: {total_squares}")
print(f"Squares with z=0 tiles: {z0_squares}")
print(f"Coverage: {z0_squares / total_squares * 100:.2f}%")

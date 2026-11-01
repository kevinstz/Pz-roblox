import sys
import os
from collections import Counter

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)

# Count tile name prefixes at z=0
prefixes = Counter()
full_names = Counter()
for (x, y, z), names in squares.items():
    if z == 0:
        for n in names:
            p = n.split('_')[0] + '_' + n.split('_')[1] if '_' in n else n
            prefixes[p] += 1
            full_names[n] += 1

print("Top 25 tile prefixes at z=0:")
for p, c in prefixes.most_common(25):
    print(f"  {p:<30}: {c}")

print("\nTop 25 full tile names at z=0:")
for n, c in full_names.most_common(25):
    print(f"  {n:<35}: {c}")

import sys, os
from collections import Counter

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex
from test_all_mats import unique_stacks, get_material_and_color

unmapped = [s[0] for s in unique_stacks if get_material_and_color(s[0])[0] == 272]
print("Unique base names falling back to 272:", len(set(unmapped)))
for n in sorted(set(unmapped))[:30]:
    print(" ", n)

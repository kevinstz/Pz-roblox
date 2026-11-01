import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex, load_all_tiles
import os
from PIL import Image
import numpy as np
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

def ascii_art(arr, w=24, h=16):
    im = Image.fromarray(arr).resize((w, h), Image.BILINEAR)
    data = np.array(im)
    out = []
    for r in range(h):
        line = ""
        for c in range(w):
            val = data[r, c]
            if val > 150:
                line += "#"
            elif val > 50:
                line += "."
            else:
                line += " "
        out.append(line)
    return "\n".join(out)

for name in ['blends_natural_01_0', 'blends_natural_01_8', 'blends_natural_01_16', 'blends_natural_01_32',
             'blends_natural_01_48', 'blends_natural_01_64',
             'blends_street_01_0', 'blends_street_01_8', 'blends_street_01_16', 'blends_street_01_48',
             'blends_street_01_54', 'blends_street_01_102']:
    spr = packs.sprite(name)
    if spr is None:
        print(f"{name}: None")
        continue
    unp = floor_image(spr)
    arr_raw = np.array(spr)[:, :, 3]
    arr_unp = np.array(unp)[:, :, 3]
    print(f"=== {name} Raw Diamond ===")
    print(ascii_art(arr_raw[192:256, :], 24, 12))
    print(f"=== {name} Unprojected ===")
    print(ascii_art(arr_unp, 20, 20))
    print("=" * 40)

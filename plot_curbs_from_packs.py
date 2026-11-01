import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex, load_all_tiles
import os
from PIL import Image
import numpy as np

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

from pzlib.iso import floor_image

for i in [0, 1, 2, 3, 40, 41, 42, 43]:
    n = f'street_curbs_01_{i}'
    spr = packs.sprite(n)
    if spr is None:
        print(f"{n}: not found in pack")
        continue
    unp = floor_image(spr)
    arr_raw = np.array(spr)[:, :, 3]
    arr_unp = np.array(unp)[:, :, 3]
    print(f"=== {n} Raw Diamond ===")
    print(ascii_art(arr_raw[192:256, :], 24, 12))
    print(f"=== {n} Current Unprojected ===")
    print(ascii_art(arr_unp, 20, 20))
    print("=" * 40)

import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex
import os
from PIL import Image
import numpy as np
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

def ascii_art(arr, w=20, h=14):
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

for i in range(64, 76):
    name = f'blends_street_01_{i}'
    spr = packs.sprite(name)
    if spr is None:
        continue
    unp = floor_image(spr)
    arr_unp = np.array(unp)
    alpha = arr_unp[:, :, 3]
    rgb = arr_unp[:, :, :3]
    mean_rgb = rgb[alpha > 50].mean(axis=0).astype(int) if (alpha > 50).any() else [0, 0, 0]
    print(f"=== {name}: alpha_mean={alpha.mean():.1f}, RGB={mean_rgb} ===")
    print(ascii_art(alpha, 20, 10))

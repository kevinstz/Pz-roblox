import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex
from PIL import Image
import numpy as np
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

def ascii_art(arr, w=20, h=10):
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

for name in ['blends_natural_01_17', 'blends_natural_01_18', 'blends_natural_01_19',
             'blends_natural_01_20', 'blends_natural_01_21', 'blends_natural_01_22',
             'blends_natural_01_23', 'blends_natural_01_24', 'blends_natural_01_25']:
    spr = packs.sprite(name)
    if spr is None:
        continue
    unp = floor_image(spr)
    arr_raw = np.array(spr)[:, :, 3]
    arr_unp = np.array(unp)[:, :, 3]
    print(f"=== {name} Unprojected ===")
    print(ascii_art(arr_unp, 20, 8))
    print("=" * 40)

import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex, load_all_tiles
from PIL import Image
import numpy as np

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])
props = load_all_tiles()

for n in ['blends_natural_01_16', 'blends_natural_01_17', 'blends_natural_01_32', 'blends_natural_01_64',
          'blends_natural_01_0', 'blends_street_01_16', 'blends_street_01_48']:
    spr = packs.sprite(n)
    p = props.get(n, {})
    if spr is not None:
        arr = np.array(spr)
        mask = arr[:, :, 3] > 50
        rgb = arr[mask, :3].mean(axis=0).astype(int) if mask.any() else [0,0,0]
        print(f"{n:<25}: props={p} mean_RGB={rgb}")

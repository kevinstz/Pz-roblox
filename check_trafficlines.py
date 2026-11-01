import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex
from PIL import Image
import numpy as np
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

spr = packs.sprite('street_trafficlines_01_0')
if spr:
    unp = floor_image(spr)
    arr = np.array(unp)
    print("trafficlines_01_0: shape=", arr.shape, "alpha_mean=", arr[:, :, 3].mean(), "RGB=", arr[arr[:, :, 3] > 50, :3].mean(axis=0))

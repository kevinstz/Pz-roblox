import sys
import os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex
from pzlib.iso import floor_image
from PIL import Image
import numpy as np

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

spr = packs.sprite('blends_street_01_96')
unp = floor_image(spr)
arr = np.array(unp)
alpha = arr[:, :, 3]
print("Shape:", alpha.shape)
print("Min alpha:", alpha.min(), "Max alpha:", alpha.max())
print("How many pixels have alpha == 0?", (alpha == 0).sum())
print("Where are they?")
ys, xs = np.nonzero(alpha == 0)
if len(xs) > 0:
    print(f"y in [{ys.min()}, {ys.max()}], x in [{xs.min()}, {xs.max()}]")

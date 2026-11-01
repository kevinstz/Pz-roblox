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
mask = arr[:, :, 3] < 200
print("Pixels < 200:", mask.sum())
mean_rgb = arr[arr[:, :, 3] > 200, :3].mean(axis=0).astype(np.uint8)
print("Mean RGB:", mean_rgb)
arr[mask, :3] = mean_rgb
arr[mask, 3] = 255
fixed = Image.fromarray(arr)
print("New min alpha:", fixed.getextrema()[3])

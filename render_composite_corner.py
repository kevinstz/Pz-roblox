import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, PackIndex
import os
from PIL import Image
import numpy as np
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
squares, rooms, headers = load_region(MAPDIR, 8040, 11585, 8165, 11760)

# Create a composite 2D image of (8096..8105, 11677..11686)
# Each tile is 128x128
nx = 8105 - 8096 + 1 # 10 tiles
ny = 11686 - 11677 + 1 # 10 tiles
canvas = Image.new('RGBA', (nx * 128, ny * 128), (0, 0, 0, 0))

for y in range(11677, 11687):
    for x in range(8096, 8106):
        sq = squares.get((x, y, 0), [])
        px = (x - 8096) * 128
        py = (y - 11677) * 128
        for n in sq:
            spr = packs.sprite(n)
            if spr is not None and spr.getbbox() and spr.getbbox()[1] >= 180:
                unp = floor_image(spr)
                canvas.paste(unp, (px, py), unp)

canvas.save(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\dbg_composite_corner.png")
print("Saved dbg_composite_corner.png, size:", canvas.size)

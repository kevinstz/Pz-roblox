import sys, os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import PackIndex

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

spr = packs.sprite('blends_grassoverlays_01_29')
print('blends_grassoverlays_01_29:', spr.size, spr.getbbox())

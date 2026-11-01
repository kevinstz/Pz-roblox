import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex
from pzlib.iso import floor_image, TextureStore
import os

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

store = TextureStore(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures')

target_hash = '273e5f7e5805a54d994e'
found = []
for name in ['blends_street_01_69', 'blends_street_01_58', 'overlay_grime_floor_01_37', 'street_curbs_01_11', 'blends_street_01_70']:
    spr = packs.sprite(name)
    if spr is not None:
        im = floor_image(spr)
        # get hash
        h = store.put(im).split('//pz42/')[1].split('.png')[0]
        print(f"{name:<30} -> {h}")
        if h == target_hash:
            found.append(name)

print("Matched:", found)

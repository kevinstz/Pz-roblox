import sys
import os
from PIL import Image

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import PackIndex, load_all_tiles

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack'])
props = load_all_tiles()

tiles_to_check = [
    'blends_street_01_96',
    'blends_street_01_101',
    'blends_street_01_103',
    'blends_street_01_102',
    'blends_street_01_48',
    'blends_street_01_54',
    'blends_natural_01_32',
    'blends_natural_01_37',
    'street_curbs_01_0',
    'street_curbs_01_1',
    'street_curbs_01_4',
    'blends_grassoverlays_01_0',
    'blends_grassoverlays_01_1'
]

for name in tiles_to_check:
    p = props.get(name, {})
    spr = packs.sprite(name)
    print(f"=== {name} ===")
    print(f"  Props: {p}")
    if spr:
        print(f"  Sprite size: {spr.size}, bbox: {spr.getbbox()}")
        spr.save(f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_check_{name}.png")
    else:
        print("  Sprite NOT FOUND in packs!")

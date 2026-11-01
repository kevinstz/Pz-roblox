import sys
import os
from PIL import Image

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import PackIndex
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack'])

# Save sample blend sprites and their de-projected floor_image
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

for prefix in ['blends_street_01', 'blends_natural_01', 'street_curbs_01']:
    for i in range(16):
        name = f"{prefix}_{i}"
        spr = packs.sprite(name)
        if spr:
            spr.save(os.path.join(out_dir, f"dbg_raw_{name}.png"))
            unproj = floor_image(spr, size=128)
            unproj.save(os.path.join(out_dir, f"dbg_unproj_{name}.png"))
            print(f"Processed {name}: raw size={spr.size}, unproj bbox={unproj.getbbox()}")

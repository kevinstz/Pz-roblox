import sys
import numpy as np
from PIL import Image

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import PackIndex

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack'])

for name in ['floors_exterior_natural_01_0', 'blends_natural_01_0', 'floors_exterior_street_01_0', 'blends_street_01_0', 'blends_grassoverlays_01_0']:
    spr = packs.sprite(name)
    if spr:
        bbox = spr.getbbox()
        arr = np.array(spr)
        alpha = arr[:, :, 3]
        nz = np.where(alpha > 0)
        y_min, y_max = nz[0].min(), nz[0].max()
        x_min, x_max = nz[1].min(), nz[1].max()
        print(f"{name}: size={spr.size}, bbox={bbox}, X range=[{x_min}..{x_max}], Y range=[{y_min}..{y_max}]")
        # Save sprite
        spr.save(f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_spr_{name}.png")

import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.assets import MEDIA, PackIndex
import os
from PIL import Image
import numpy as np
from pzlib.iso import floor_image

packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

corner_curbs = [
    ('y78_x97', 'street_curbs_01_diag_44'),
    ('y78_x98', 'street_curbs_01_diag_46'),
    ('y79_x99', 'street_curbs_01_49'),
    ('y80_x00', 'street_curbs_01_diag_16'),
    ('y81_x00', 'street_curbs_01_diag_11'),
    ('y81_x01', 'street_curbs_01_diag_1'),
    ('y82_x01', 'street_curbs_01_diag_19'),
    ('y83_x01', 'street_curbs_01_diag_20'),
    ('y84_x01', 'street_curbs_01_diag_2_53'),
    ('y85_x01', 'street_curbs_01_diag_2_40'),
]

for label, name in corner_curbs:
    spr = packs.sprite(name)
    if spr is None:
        print(f"{name}: None")
        continue
    unp = floor_image(spr)
    arr_raw = np.array(spr)
    arr_unp = np.array(unp)
    raw_alpha = arr_raw[192:256, :, 3]
    unp_alpha = arr_unp[:, :, 3]
    # save unp image for visual inspection
    unp.save(f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_unp_{name}.png")
    print(f"Saved dbg_unp_{name}.png: raw_bbox={spr.getbbox()}, unp_bbox={unp.getbbox()}")

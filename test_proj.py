import math
import numpy as np

# Camera math for Roblox camera:
# In frame 6, character is at screen (977, 454). Image size is (1080, 1920) (H, W).
# Screen center is (960, 540).
# Let's find parts that are in the view.
from dump_pair2_region import dump_pair2_region
found = dump_pair2_region()

# Let's search for parts that have Size, Name, or Decals matching that white arch:
# In white_obj_crop2.jpg, the white structure has an arch molding on it!
# Arch moldings in PZ:
# "fixtures_doors_frames_...", "walls_detailing_...", "location_...", "street_decoration_...", "fixtures_windows_..."
for p in found:
    name = p[0].lower()
    txt = p[6]
    if any(k in name for k in ['arch', 'door', 'pediment', 'frame', 'white', 'pillar', 'column', 'detailing_01_24', 'detailing_01_25', 'detailing_01_26']):
        if -60 <= p[2] <= -40 and -75 <= p[4] <= -55:
            print(f"Ref={p[7]} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Parent={p[5]}")

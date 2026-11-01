from PIL import Image
import numpy as np

# Inspect dbg_unproj_blends_street_01_10.png
for name in ['blends_street_01_10', 'blends_street_01_11', 'street_curbs_01_0', 'street_curbs_01_1', 'street_curbs_01_4', 'blends_natural_01_8', 'blends_natural_01_9']:
    p = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_unproj_{name}.png"
    im = Image.open(p)
    arr = np.array(im)
    alpha = arr[:, :, 3]
    # Check which corners have alpha > 0
    tl = alpha[0, 0] > 0
    tr = alpha[0, -1] > 0
    bl = alpha[-1, 0] > 0
    br = alpha[-1, -1] > 0
    print(f"{name:<25}: TL={tl}, TR={tr}, BL={bl}, BR={br}, mean alpha={alpha.mean():.1f}")

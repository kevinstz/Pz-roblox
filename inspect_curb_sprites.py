from PIL import Image
import numpy as np

# Load raw curb images and print their visual shape
# In PZ, let's see which pixels are non-transparent in dbg_raw_street_curbs_01_0.png, 1, 4
for i in [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15]:
    p = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_raw_street_curbs_01_{i}.png"
    im = Image.open(p)
    arr = np.array(im)
    alpha = arr[:, :, 3]
    # diamond is at y: 192..256, x: 0..128
    d_alpha = alpha[192:256, :]
    ys, xs = np.nonzero(d_alpha > 50)
    if len(xs) > 0:
        print(f"Curb {i:2d}: bbox in diamond x=[{xs.min()}:{xs.max()}], y=[{ys.min()}:{ys.max()}], count={len(xs)}")

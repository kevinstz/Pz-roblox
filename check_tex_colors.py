from PIL import Image
import numpy as np

tex_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"
hashes = {
    'blends_street_01_96': 'a8a5c370590b10b7fab3',
    'blends_street_01_101': '9f722cda42b3e8299dab',
    'blends_street_01_102': '7b5a7835f5ededb9039b',
    'blends_street_01_103': 'ff5ca3c4ea2334782a2f',
    'blends_street_01_48': '5b739f8939cb952826d4',
}

for name, h in hashes.items():
    p = f"{tex_dir}\\{h}.png"
    im = Image.open(p)
    arr = np.array(im)
    print(f"{name}: shape={arr.shape}, mean RGB={arr[:, :, :3].mean(axis=(0, 1)).astype(int)}, mean A={arr[:, :, 3].mean():.1f}")

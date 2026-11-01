import cv2
import numpy as np

for name in ['tex_67cf.png', 'tex_a25c.png', 'tex_d085.png', 'tex_e880.png', 'tex_237f.png']:
    img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    if img is not None:
        print(f"{name}: shape={img.shape}, dtype={img.dtype}, mean_bgr={np.mean(img[:,:,:3], axis=(0,1))}")

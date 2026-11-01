import cv2
import numpy as np

img = cv2.imread('ref_target_bld.jpg')
# Let's save a thumbnail or check the colors across rows
h, w, _ = img.shape
print(f"h={h}, w={w}")

# In ref_target_bld, let's find the upper wall / parapet
# Let's check mean BGR in several horizontal slices
for y in range(0, h, 50):
    slice_img = img[y:y+50, :]
    print(f"y={y:3d}..{y+50:3d} | mean BGR = {np.mean(slice_img, axis=(0,1))}")

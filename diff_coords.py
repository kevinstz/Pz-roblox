import cv2
import numpy as np

vp10 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp10_full.jpg")
vp11 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp11_full.jpg")

diff = np.abs(vp10.astype(float) - vp11.astype(float)).mean(axis=2)
# Threshold diff > 20
mask = diff > 20

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\diff_mask_10_11.jpg", (mask * 255).astype(np.uint8))

ys, xs = np.where(mask)
print(f"Diff Y range: min={ys.min()}, max={ys.max()}")
print(f"Diff X range: min={xs.min()}, max={xs.max()}")

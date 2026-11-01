import cv2
import os
import numpy as np

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
img10 = cv2.imread(os.path.join(dense_dir, "dense_10_2.83s.jpg"))
img11 = cv2.imread(os.path.join(dense_dir, "dense_11_3.12s.jpg"))

vp10 = img10[150:890, 0:1500]
vp11 = img11[150:890, 0:1500]

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp10_full.jpg", vp10)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp11_full.jpg", vp11)
print("Saved vp10_full.jpg and vp11_full.jpg")

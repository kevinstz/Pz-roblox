import cv2
import numpy as np

# Let's inspect v4_tile_r2_c0.jpg and v4_tile_r1_c0.jpg in detail
img_r2c0 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\v4_tile_r2_c0.jpg")
img_r1c0 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\v4_tile_r1_c0.jpg")

print("r2c0 shape:", img_r2c0.shape)
print("r1c0 shape:", img_r1c0.shape)

import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_flicker_dense10.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_flicker_dense11.jpg')

print("Flicker10 shape:", img10.shape)
print("Flicker11 shape:", img11.shape)

# Let's compare the difference
diff = cv2.absdiff(img10, img11)
print("Mean diff per channel (B, G, R):", diff.mean(axis=(0,1)))

# Let's see if 3D objects (trees, benches, lights) are in flicker11!
# In flicker11, where is it NOT green?
# Green in flicker11 has BGR ~ (38, 87, 69)
# Let's find pixels in flicker11 that differ significantly from this green background:
green_bg = np.array([38, 87, 69], dtype=np.float32)
dist_from_green = np.linalg.norm(img11.astype(np.float32) - green_bg, axis=2)
non_green_in_11 = (dist_from_green > 35)

print("Percentage of non-green pixels in flicker11:", np.count_nonzero(non_green_in_11) / non_green_in_11.size * 100)

# What are those non-green pixels in flicker11?
# Let's check if there are trees, picnic table, street lamp, etc.

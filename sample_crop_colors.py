import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_inspect_area.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop11_inspect_area.jpg')

# Let's print out what features exist in crop10
# For example, are there white lines? Curbs? Pavement?
print("Crop10 shape:", img10.shape)
# Street asphalt color in crop10:
# Let's sample a few points in crop10:
for y in [50, 100, 150]:
    for x in [50, 150, 250, 350]:
        print(f"crop10 (y={y}, x={x}): BGR = {img10[y, x]}, crop11: BGR = {img11[y, x]}")

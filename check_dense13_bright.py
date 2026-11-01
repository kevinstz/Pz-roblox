import cv2
import numpy as np

img13 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\thumb_dense13_full.jpg')
# What is the color of the dark region [37, 36, 33]?
# In Roblox Studio, is that the dark theme background of the editor when out of bounds or is it night time?
# Let's check Lighting.TimeOfDay or is the camera looking outside the map?
# Let's check the bottom of img13 where Bot BGR is [119, 115, 106]:
h, w, _ = img13.shape
print("img13 shape:", h, w)

# Find the boundary between dark and bright in img13:
gray13 = cv2.cvtColor(img13, cv2.COLOR_BGR2GRAY)
bright_mask = gray13 > 60
print("Percentage of screen bright in dense13:", bright_mask.sum() / bright_mask.size * 100)

y_bright, x_bright = np.where(bright_mask)
if len(y_bright) > 0:
    print(f"Bright region Y: {y_bright.min()} to {y_bright.max()}")
    print(f"Bright region X: {x_bright.min()} to {x_bright.max()}")

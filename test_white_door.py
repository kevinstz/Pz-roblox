import cv2
import numpy as np

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_real_white_door.jpg")
print("Crop real white door shape:", img.shape)
# Mean color
print("Mean BGR:", np.mean(img, axis=(0,1)))
# Look for white pixels
white_mask = (img[:,:,0] > 200) & (img[:,:,1] > 200) & (img[:,:,2] > 200)
print("White pixel count:", np.sum(white_mask))

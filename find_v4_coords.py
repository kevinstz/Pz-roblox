import cv2
import numpy as np

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_006_2.90s.jpg")
print("Image shape:", img.shape)

# Let's crop the bottom half of the image into a grid of 4x4 thumbnails to find where everything is
h, w, _ = img.shape
grid = cv2.resize(img, (960, 540))
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\v4_half.jpg", grid)
print("Saved v4_half.jpg")

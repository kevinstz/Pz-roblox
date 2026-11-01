import cv2
import numpy as np

tl = cv2.imread("v4_crop_top_left.jpg")
print("Top-left shape:", tl.shape)
# Let's save a smaller thumbnail to check
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\v4_tl_thumb.jpg", cv2.resize(tl, (480, 270)))

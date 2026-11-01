import cv2
import numpy as np

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\v4_tile_r2_c0.jpg")
h, w, _ = img.shape
# The white object is around x in [350, 500], y in [150, 360]
white_obj = img[150:360, 350:500]
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\white_obj_v4.jpg", white_obj)
print("Saved white_obj_v4.jpg, shape:", white_obj.shape)

# Let's inspect its colors:
# It's bright grey/white, around BGR 210, 215, 220
print("Mean BGR of white object:", np.mean(white_obj[white_obj > 150]))

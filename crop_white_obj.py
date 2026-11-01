import cv2
import numpy as np

# In v4_f6_center.jpg, the white structure is at the bottom left:
img6 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_006_2.90s.jpg")
# In v4_f6_center.jpg, crop was img6[100:800, 400:1500]
# Bottom left of crop corresponds to y around 700:800, x around 400:550 in img6!
crop_white = img6[650:800, 400:600]
cv2.imwrite("white_obj_crop.jpg", crop_white)
print("Saved white_obj_crop.jpg")

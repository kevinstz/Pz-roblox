import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')

# Template from static building in 10
tmpl = img10[350:450, 1250:1350]
res = cv2.matchTemplate(img11, tmpl, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

print("Best match score:", max_val)
print("Shift in pixels: dx =", max_loc[0] - 1250, "dy =", max_loc[1] - 350)

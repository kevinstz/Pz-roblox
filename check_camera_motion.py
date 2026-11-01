import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')

# 1. Let's find the cursor position in frame 10 vs frame 11
# IsoCursor is a white reticle / ring
# Let's crop 100x100 around player in 10 and 11:
crop10_char = img10[600:720, 900:1020]
crop11_char = img11[600:720, 900:1020]

cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_char.jpg', crop10_char)
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop11_char.jpg', crop11_char)

# 2. Let's check the position of static world objects in frame 10 vs frame 11:
# A lamppost or building corner that didn't move!
# Medical clinic roof corner or building at (x=1200..1400, y=300..500)
crop10_bld = img10[300:500, 1200:1400]
crop11_bld = img11[300:500, 1200:1400]

diff_bld = cv2.absdiff(crop10_bld, crop11_bld)
print("Mean diff on static building (B, G, R):", diff_bld.mean(axis=(0,1)))

# If mean diff is near 0, the camera DID NOT MOVE AT ALL!

import cv2
import os

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'
f = [x for x in os.listdir(p_dir) if x.startswith('dense_13')][0]
img = cv2.imread(f"{p_dir}\\{f}")
thumb = cv2.resize(img, (960, 540))
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\thumb_dense13_full.jpg', thumb)

# Also let's inspect dense_00
f0 = [x for x in os.listdir(p_dir) if x.startswith('dense_00')][0]
img0 = cv2.imread(f"{p_dir}\\{f0}")
thumb0 = cv2.resize(img0, (960, 540))
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\thumb_dense00_full.jpg', thumb0)

print("Saved thumb_dense13_full and thumb_dense00_full.")

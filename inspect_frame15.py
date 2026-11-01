import cv2
import os

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'
f = [x for x in os.listdir(p_dir) if x.startswith('dense_15')][0]
img = cv2.imread(f"{p_dir}\\{f}")

# Crop viewport center
crop = img[200:800, 400:1600]
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_frame15.jpg', crop)
print("Saved crop_frame15.jpg")

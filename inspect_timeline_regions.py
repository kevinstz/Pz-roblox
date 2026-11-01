import cv2
import numpy as np

# Let's inspect dense_13, dense_16, dense_20, dense_22
p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'

for idx in [0, 2, 7, 10, 11, 13, 16, 20, 22]:
    f = f"dense_{idx:02d}_{idx*0.283:.2f}s.jpg"
    img = cv2.imread(f"{p_dir}\\{f}")
    if img is not None:
        # Check center 200x200
        center = img[440:640, 860:1060].mean(axis=(0,1))
        # Check top 200x200
        top = img[100:300, 860:1060].mean(axis=(0,1))
        # Check bottom 200x200
        bot = img[780:980, 860:1060].mean(axis=(0,1))
        print(f"[{idx:02d}] Top BGR: {top.astype(int)}, Center BGR: {center.astype(int)}, Bot BGR: {bot.astype(int)}")

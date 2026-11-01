import cv2
import os
import numpy as np

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
files = sorted([f for f in os.listdir(dense_dir) if f.endswith(".jpg")])

# In each frame, find the purple wings / bee character
# The purple wings have high B and R, low G: B > 150, R > 100, G < 80
for fn in files:
    img = cv2.imread(os.path.join(dense_dir, fn))
    vp = img[150:890, 0:1500]
    
    # Mask purple
    b = vp[:, :, 0]
    g = vp[:, :, 1]
    r = vp[:, :, 2]
    purple_mask = (b > 130) & (r > 100) & (g < 100)
    ys, xs = np.where(purple_mask)
    if len(xs) > 0:
        cx, cy = int(xs.mean()), int(ys.mean())
        print(f"{fn}: Player at ({cx}, {cy}), purple pixels: {len(xs)}")
    else:
        print(f"{fn}: Player NOT found!")

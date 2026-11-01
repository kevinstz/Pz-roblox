import cv2
import numpy as np
import os

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'

# Let's inspect dense_02, dense_04, dense_07, dense_10, dense_11
for fname in ['dense_02_0.57s.jpg', 'dense_04_1.13s.jpg', 'dense_07_1.98s.jpg', 'dense_10_2.83s.jpg', 'dense_11_3.12s.jpg']:
    img = cv2.imread(os.path.join(p_dir, fname))
    h, w, _ = img.shape
    # Check horizontal strip across the screen at y=250 (width 200..1200)
    strip = img[220:260, 200:1200]
    mean_b = strip[:, :, 0].mean()
    mean_g = strip[:, :, 1].mean()
    mean_r = strip[:, :, 2].mean()
    print(f"{fname}: (h={h}, w={w}) strip y=220..260 BGR = ({mean_b:.1f}, {mean_g:.1f}, {mean_r:.1f})")

# Let's find the exact horizontal boundary in dense_02 or dense_11!
img11 = cv2.imread(os.path.join(p_dir, 'dense_11_3.12s.jpg'))
img10 = cv2.imread(os.path.join(p_dir, 'dense_10_2.83s.jpg'))
diff = cv2.absdiff(img10, img11)
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

# Sum across columns to find where difference occurs along Y
row_sum = (gray > 25).sum(axis=1)
for y in range(0, h, 20):
    cnt = (gray[y:y+20, :] > 25).sum()
    print(f"y={y:3d}..{y+20:3d}: changed pixels = {cnt}")

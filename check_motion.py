import cv2
import os
import numpy as np

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
files = sorted([f for f in os.listdir(dense_dir) if f.endswith(".jpg")])

for i in range(len(files)-1):
    f1 = cv2.imread(os.path.join(dense_dir, files[i]))
    f2 = cv2.imread(os.path.join(dense_dir, files[i+1]))
    # Crop viewport
    vp1 = f1[150:890, 0:1500]
    vp2 = f2[150:890, 0:1500]
    diff = np.abs(vp1.astype(float) - vp2.astype(float)).mean()
    print(f"{files[i]} -> {files[i+1]}: viewport diff = {diff:.2f}")

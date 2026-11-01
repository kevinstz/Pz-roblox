import cv2
import os
import numpy as np

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'
frames = sorted(os.listdir(p_dir))

for i, f in enumerate(frames):
    img = cv2.imread(os.path.join(p_dir, f))
    # Area in question: y=200..300, x=800..1200
    sub = img[200:300, 800:1200]
    # Check if green or grey
    # Green: B < 60, G > 70
    # Grey: B > 80, G > 80, R > 80
    b, g, r = sub[:, :, 0].mean(), sub[:, :, 1].mean(), sub[:, :, 2].mean()
    status = "GREEN (MISSING)" if (b < 60 and g > 65) else "GREY (RENDERED)" if (b > 75 and g > 75) else "OTHER"
    print(f"[{i:02d}] {f}: BGR=({b:5.1f}, {g:5.1f}, {r:5.1f}) -> {status}")

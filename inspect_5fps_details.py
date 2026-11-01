import cv2
import os
import numpy as np

d = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\video3_5fps"
frames = sorted(os.listdir(d))

for f in frames:
    img = cv2.imread(os.path.join(d, f))
    # Area y=200..300, x=800..1200
    sub = img[200:300, 800:1200]
    b, g, r = sub[:, :, 0].mean(), sub[:, :, 1].mean(), sub[:, :, 2].mean()
    status = "MISSING" if (b < 60 and g > 65) else "RENDERED" if (b > 75 and g > 75) else "OTHER"
    
    # Bee avatar yellow stripes
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, (18, 120, 120), (32, 255, 255))
    y_idx, x_idx = np.where(yellow_mask > 0)
    if len(y_idx) > 0:
        pos_str = f"bee=({int(np.mean(x_idx)):4d}, {int(np.mean(y_idx)):4d})"
    else:
        pos_str = "bee=NOT DETECTED"
        
    print(f"{f}: {pos_str} | ground={status} (BGR={b:.0f},{g:.0f},{r:.0f})")

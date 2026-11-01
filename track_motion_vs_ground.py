import cv2
import os
import numpy as np

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'
frames = sorted(os.listdir(p_dir))

for i, f in enumerate(frames):
    img = cv2.imread(os.path.join(p_dir, f))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Bee avatar yellow stripes
    yellow_mask = cv2.inRange(hsv, (18, 120, 120), (32, 255, 255))
    y_idx, x_idx = np.where(yellow_mask > 0)
    
    # Area y=200..300, x=800..1200
    sub = img[200:300, 800:1200]
    b, g, r = sub[:, :, 0].mean(), sub[:, :, 1].mean(), sub[:, :, 2].mean()
    status = "MISSING" if (b < 60 and g > 65) else "RENDERED" if (b > 75 and g > 75) else "OTHER"
    
    if len(y_idx) > 0:
        pos_str = f"bee=(x={int(np.mean(x_idx)):4d}, y={int(np.mean(y_idx)):4d})"
    else:
        pos_str = "bee=NOT DETECTED"
        
    print(f"[{i:02d}] {f[:8]}: {pos_str} | ground={status}")

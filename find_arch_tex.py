import os
import cv2
import numpy as np

# Let us find which texture in out/textures contains an arch or looks like the arch in crop_real_white_door.jpg
arch_crop = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_real_white_door.jpg")

tex_dir = r"out\textures"
matches = []

for f in os.listdir(tex_dir):
    if f.endswith('.png'):
        p = os.path.join(tex_dir, f)
        img = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        if img is None: continue
        h, w = img.shape[:2]
        # In crop_real_white_door, the arch has an arched top with pilasters/columns on left and right
        # Let's check aspect ratio or if it has white pixels with arched shape:
        if 50 <= h <= 400 and 30 <= w <= 200:
            # check if it has lots of white/light pixels (>200)
            if img.shape[2] == 4:
                rgb = img[:,:,:3]
                alpha = img[:,:,3]
                white_px = (rgb[:,:,0] > 180) & (rgb[:,:,1] > 180) & (rgb[:,:,2] > 180) & (alpha > 100)
                if np.sum(white_px) > 1000:
                    matches.append((f, h, w, np.sum(white_px)))

print(f"Total matching white textures: {len(matches)}")
for m in sorted(matches, key=lambda x: -x[3])[:15]:
    print(m)

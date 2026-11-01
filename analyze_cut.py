import cv2
import os
import numpy as np

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
files = sorted([f for f in os.listdir(dense_dir) if f.endswith(".jpg")])

for i, fn in enumerate(files):
    img = cv2.imread(os.path.join(dense_dir, fn))
    # Check line y=300 (where the horizontal cut happens in vp_02)
    # in viewport (y from 150 to 890, so y=150+150 = 300)
    vp = img[150:890, 0:1500]
    # Check mean color of row 100 vs row 200 in vp
    # Row 100 is above the cut (y=250 in img)
    # Row 200 is below the cut (y=350 in img)
    row_above = vp[100, 300:700].mean(axis=0) # [B, G, R]
    row_below = vp[200, 300:700].mean(axis=0)
    
    # If row_above is green (G > R and G > B), it's the grass terrain!
    is_grass_above = row_above[1] > row_above[0] + 15 and row_above[1] > row_above[2] + 15
    print(f"{fn}: Row above G={row_above[1]:.1f}, R={row_above[2]:.1f}, B={row_above[0]:.1f} -> {'CUTOFF (GRASS)' if is_grass_above else 'RENDERED (ROAD)'}")

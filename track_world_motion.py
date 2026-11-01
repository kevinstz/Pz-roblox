import cv2
import os
import numpy as np

d = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\video3_5fps"

# In each frame, let's track the position of a landmark on the ground
# For example, a white parking stripe or manhole or curb line
# That tells us the EXACT camera motion!
# Let's crop a landmark in f_002:
img02 = cv2.imread(os.path.join(d, "f_002_0.37s.jpg"))
# There are parking lot lines at the bottom right
# Let's find parking stripes or curbs
print("Tracking camera motion across frames:")

# Let's use template matching on a distinct feature in the lower screen (e.g. curb or parking line)
# In f_006 (rendered), let's pick a template at (x=1300..1400, y=700..800)
tmpl = img02[750:850, 600:700]
h_t, w_t, _ = tmpl.shape

prev_loc = (600, 750)
for i in range(2, 20):
    fname = f"f_{i:03d}_{i*0.183:.2f}s.jpg"
    img = cv2.imread(os.path.join(d, fname))
    if img is None: continue
    
    # Search around prev_loc
    res = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF_NORMED)
    min_v, max_v, min_l, max_l = cv2.minMaxLoc(res)
    dx = max_l[0] - 600
    dy = max_l[1] - 750
    print(f"{fname}: shift from f_002 = (dx={dx:3d}, dy={dy:3d}) | match={max_v:.2f}")

import cv2
import os
import numpy as np

timeline_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\video_timeline"
files = sorted([f for f in os.listdir(timeline_dir) if f.endswith(".jpg")])

# Grid of 4 rows, 6 cols (24 cells)
cell_w, cell_h = 320, 160
grid = np.zeros((cell_h * 4, cell_w * 6, 3), dtype=np.uint8)

for i, fn in enumerate(files):
    img = cv2.imread(os.path.join(timeline_dir, fn))
    resized = cv2.resize(img, (cell_w, cell_h))
    # Draw step index
    cv2.putText(resized, f"{i:02d}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    r = i // 6
    c = i % 6
    grid[r*cell_h:(r+1)*cell_h, c*cell_w:(c+1)*cell_w] = resized

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\montage_all_steps.jpg", grid)
print("Saved montage_all_steps.jpg")

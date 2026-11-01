import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')

diff = cv2.absdiff(img10, img11)
# Save diff visualization
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\diff_10_11_vis.jpg', diff * 3)

# Find bounding box of changed region
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
thresh = (gray > 20).astype(np.uint8)

y_indices, x_indices = np.where(thresh > 0)
if len(y_indices) > 0:
    min_x, max_x = x_indices.min(), x_indices.max()
    min_y, max_y = y_indices.min(), y_indices.max()
    print(f"Diff bounding box: X=[{min_x}, {max_x}], Y=[{min_y}, {max_y}]")
    print(f"Total changed pixels: {len(y_indices)}")
    
    # Check bottom-most line of change
    # Is it a straight line or jagged?
    # For each column x, what is the max y where change occurs?
    col_max_y = []
    for x in range(min_x, max_x + 1, 10):
        ys = y_indices[x_indices == x]
        if len(ys) > 0:
            col_max_y.append(ys.max())
    print(f"Max Y across columns: min={min(col_max_y)}, max={max(col_max_y)}, median={np.median(col_max_y)}")

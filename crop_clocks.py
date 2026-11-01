import cv2
import os

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
files = sorted([f for f in os.listdir(dense_dir) if f.endswith(".jpg")])

# In each frame, let's extract:
# 1. The clock in HUD (top right of viewport, around x: 1300..1480, y: 160..240)
# 2. The player position in viewport
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

for i, fn in enumerate(files):
    img = cv2.imread(os.path.join(dense_dir, fn))
    # HUD clock: x: 1250..1450, y: 155..240
    clock = img[155:240, 1250:1450]
    cv2.imwrite(os.path.join(out_dir, f"clock_{i:02d}.jpg"), clock)

print("Saved clocks.")

import cv2
import os

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
files = sorted([f for f in os.listdir(dense_dir) if f.endswith(".jpg")])

print(f"Total dense frames: {len(files)}")
# Let's check the player position or if the player moves
for f in files:
    img = cv2.imread(os.path.join(dense_dir, f))
    print(f"{f}: shape={img.shape}")

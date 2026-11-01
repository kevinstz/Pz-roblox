import cv2
import os

d = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames"
files = sorted([f for f in os.listdir(d) if f.endswith('.jpg')])

print(f"Total frames: {len(files)}")
for f in files:
    # Read frame and compute average brightness or see if scene changes
    img = cv2.imread(os.path.join(d, f))
    print(f, "shape:", img.shape)

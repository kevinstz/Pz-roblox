import cv2
import os

frames = [f"video4_frames/frame_{i:03d}_{t:.2f}s.jpg" for i, t in [
    (0, 0.0), (4, 1.87), (8, 3.87), (12, 5.80), (16, 7.73)
]]

for p in frames:
    full_path = os.path.join(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30", p)
    if os.path.exists(full_path):
        print(f"Exists: {p}")

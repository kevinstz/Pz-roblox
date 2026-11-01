import cv2
import numpy as np

# Let's track the bee character in frame 0 and frame 6
for idx, s in [(0, '0.00'), (6, '2.90')]:
    path = rf"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_{idx:03d}_{s}s.jpg"
    img = cv2.imread(path)
    # The bee has bright yellow and purple wings
    # Yellow: high R, high G, low B (e.g. B < 50, G > 180, R > 200)
    yellow = (img[:,:,0] < 80) & (img[:,:,1] > 180) & (img[:,:,2] > 200)
    pts = np.argwhere(yellow)
    if len(pts) > 0:
        cy, cx = np.mean(pts, axis=0)
        print(f"Frame {idx} ({s}s): Bee screen center = ({cx:.1f}, {cy:.1f})")
    else:
        print(f"Frame {idx} ({s}s): Bee not found by yellow mask")

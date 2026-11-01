import cv2
import os

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
files = sorted([f for f in os.listdir(dense_dir) if f.endswith(".jpg")])
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\video_timeline"
os.makedirs(out_dir, exist_ok=True)

for i, fn in enumerate(files):
    img = cv2.imread(os.path.join(dense_dir, fn))
    # Viewport region
    vp = img[150:890, 0:1500]
    # Resize to 640x316 for quick inspection
    thumb = cv2.resize(vp, (640, 316))
    cv2.imwrite(os.path.join(out_dir, f"step_{i:02d}.jpg"), thumb)

print(f"Generated {len(files)} timeline steps.")

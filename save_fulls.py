import cv2
import os

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

for idx in [0, 1, 4, 6, 8, 10, 12, 14, 20]:
    fn = [f for f in os.listdir(dense_dir) if f.startswith(f"dense_{idx:02d}_")][0]
    img = cv2.imread(os.path.join(dense_dir, fn))
    # Resize to 960x540 for fast reading
    thumb = cv2.resize(img, (960, 540))
    cv2.imwrite(os.path.join(out_dir, f"full_{idx:02d}.jpg"), thumb)

print("Saved full frames.")

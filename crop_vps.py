import cv2
import os

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

for idx in [2, 6, 10, 14, 18, 20]:
    fn = f"dense_{idx:02d}.jpg"
    # Find matching file in dense_dir
    matches = [f for f in os.listdir(dense_dir) if f.startswith(f"dense_{idx:02d}_")]
    if matches:
        img = cv2.imread(os.path.join(dense_dir, matches[0]))
        vp = img[150:890, 0:1500]
        cv2.imwrite(os.path.join(out_dir, f"vp_{idx:02d}.jpg"), vp)
        print(f"Saved vp_{idx:02d}.jpg")

import cv2
import os

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'
for f in os.listdir(p_dir):
    if f.startswith('dense_14') or f.startswith('dense_18') or f.startswith('dense_00'):
        img = cv2.imread(os.path.join(p_dir, f))
        thumb = cv2.resize(img, (640, 360))
        cv2.imwrite(rf'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\thumb_{f[:8]}.jpg', thumb)
        print(f"Saved thumb_{f[:8]}.jpg, overall BGR = {img.mean(axis=(0,1))}")

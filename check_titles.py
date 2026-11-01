import cv2
import os

p_dir = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense'

# Crop the window title bar (y: 0..40, x: 0..1000)
for idx in [0, 2, 4, 10, 11, 13, 20]:
    f = [x for x in os.listdir(p_dir) if x.startswith(f'dense_{idx:02d}')][0]
    img = cv2.imread(f"{p_dir}\\{f}")
    title = img[0:40, 0:800]
    cv2.imwrite(rf'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\title_{idx:02d}.jpg', title)

print("Saved titles.")

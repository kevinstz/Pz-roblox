import os
import cv2

tex_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\launcher\extracted\pz42"
for tname in ["3c1fa55c2b2a32f776a5.png", "8c371eff95ae6b30a562.png", "684037041b29ec20554a.png", "67cf2d4655419cf61751.png"]:
    p = os.path.join(tex_dir, tname)
    if os.path.exists(p):
        img = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        print(f"{tname}: shape={img.shape}, mean color (BGR)={img[:,:,:3].mean(axis=(0,1))}")
    else:
        print(f"{tname} not found in {tex_dir}")

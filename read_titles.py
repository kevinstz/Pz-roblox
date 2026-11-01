import cv2
import numpy as np

for idx in [0, 2, 4, 10, 11, 13, 20]:
    t = cv2.imread(rf'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\title_{idx:02d}.jpg')
    print(f"[{idx:02d}] title bar mean BGR = {t.mean(axis=(0,1))}")

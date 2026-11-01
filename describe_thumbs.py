import cv2
import numpy as np

for name in ['thumb_dense_00.jpg', 'thumb_04.jpg', 'thumb_10.jpg', 'thumb_dense_14.jpg']:
    img = cv2.imread(rf'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\{name}')
    h, w, _ = img.shape
    # Quadrants:
    tl = img[:h//2, :w//2].mean(axis=(0,1))
    tr = img[:h//2, w//2:].mean(axis=(0,1))
    bl = img[h//2:, :w//2].mean(axis=(0,1))
    br = img[h//2:, w//2:].mean(axis=(0,1))
    print(f"=== {name} ===")
    print(f"  Top-Left:  BGR=({tl[0]:.1f}, {tl[1]:.1f}, {tl[2]:.1f})")
    print(f"  Top-Right: BGR=({tr[0]:.1f}, {tr[1]:.1f}, {tr[2]:.1f})")
    print(f"  Bot-Left:  BGR=({bl[0]:.1f}, {bl[1]:.1f}, {bl[2]:.1f})")
    print(f"  Bot-Right: BGR=({br[0]:.1f}, {br[1]:.1f}, {br[2]:.1f})")

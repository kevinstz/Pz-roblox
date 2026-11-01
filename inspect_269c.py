import os
import cv2

path = r"out\textures\269c60558829ab318960.png"
if os.path.exists(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    print("Texture shape:", img.shape)
    cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\tex_269c.png", img)
    print("Saved tex_269c.png")
else:
    print("Not found:", path)

import cv2
import os

dense_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense"
img10 = cv2.imread(os.path.join(dense_dir, "dense_10_2.83s.jpg"))
img11 = cv2.imread(os.path.join(dense_dir, "dense_11_3.12s.jpg"))

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_10_raw.jpg", img10)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_11_raw.jpg", img11)
print("Saved full 10 and 11.")

import cv2
import os

d = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames"
img6 = cv2.imread(os.path.join(d, "frame_006_2.90s.jpg"))
img14 = cv2.imread(os.path.join(d, "frame_014_6.77s.jpg"))

h, w, _ = img6.shape
cv2.imwrite("v4_f6_center.jpg", img6[100:800, 400:1500])
cv2.imwrite("v4_f14_center.jpg", img14[100:800, 400:1500])
print("Saved f6 and f14 center crops")

import cv2
import os

d = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames"
img0 = cv2.imread(os.path.join(d, "frame_000_0.00s.jpg"))
print("Frame 0 shape:", img0.shape)

# Let's crop different quadrants of frame 0:
# Top-left, Top-right, Bottom-left, Bottom-right
h, w, _ = img0.shape
cv2.imwrite("v4_f0_top_left.jpg", img0[0:h//2, 0:w//2])
cv2.imwrite("v4_f0_top_right.jpg", img0[0:h//2, w//2:w])
cv2.imwrite("v4_f0_bot_left.jpg", img0[h//2:h, 0:w//2])
cv2.imwrite("v4_f0_bot_right.jpg", img0[h//2:h, w//2:w])
print("Saved 4 quadrants of frame 0")

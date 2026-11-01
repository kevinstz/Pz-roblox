import cv2
import os

d = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames"
files = sorted([f for f in os.listdir(d) if f.endswith('.jpg')])

for f in files:
    img = cv2.imread(os.path.join(d, f))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # The character wears a bright yellow bee hat/hoodie
    mask = cv2.inRange(hsv, (25, 200, 200), (35, 255, 255))
    # only search in game viewport: Y in [100, 950], X in [50, 1800]
    sub = mask[100:950, 50:1800]
    M = cv2.moments(sub)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"]) + 50
        cy = int(M["m01"] / M["m00"]) + 100
        print(f"{f}: bee at ({cx}, {cy})")
    else:
        print(f"{f}: not found")

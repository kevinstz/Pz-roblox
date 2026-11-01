import cv2
import os

d = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames"
files = sorted([f for f in os.listdir(d) if f.endswith('.jpg')])

for f in files:
    img = cv2.imread(os.path.join(d, f))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Purple backpack: H in [120, 150], S in [100, 255], V in [100, 255]
    mask = cv2.inRange(hsv, (120, 100, 100), (150, 255, 255))
    # viewport: y in [200, 900], x in [200, 1600]
    sub = mask[200:900, 200:1600]
    M = cv2.moments(sub)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"]) + 200
        cy = int(M["m01"] / M["m00"]) + 200
        print(f"{f}: character at ({cx}, {cy})")
    else:
        print(f"{f}: not found")

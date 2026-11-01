import cv2
import numpy as np

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_006_2.90s.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Bee yellow: H in [20, 35], S > 150, V > 150
yellow_mask = cv2.inRange(hsv, (20, 150, 150), (35, 255, 255))
# Bee purple: H in [130, 160], S > 100, V > 100
purple_mask = cv2.inRange(hsv, (130, 100, 100), (160, 255, 255))

for name, mask in [("yellow", yellow_mask), ("purple", purple_mask)]:
    M = cv2.moments(mask)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        print(f"Bee {name} center: ({cx}, {cy})")
    else:
        print(f"Bee {name} mask empty")

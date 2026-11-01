import cv2
import numpy as np

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_004_1.93s.jpg")

# Find where blue car is: blue color in HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blue_mask = cv2.inRange(hsv, (100, 100, 100), (130, 255, 255))
M = cv2.moments(blue_mask)
if M["m00"] > 0:
    cx_blue = int(M["m10"] / M["m00"])
    cy_blue = int(M["m01"] / M["m00"])
    print(f"Blue car center: ({cx_blue}, {cy_blue})")
else:
    print("Blue car mask empty")

# Black car is nearby: let's print where it is
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_cars.jpg", img[300:600, 950:1500])

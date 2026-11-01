import cv2
import numpy as np

img25 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f25.jpg")
img06 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f06.jpg")
h, w, _ = img25.shape
print("img25 shape:", h, w)

diff = cv2.absdiff(img06, img25)
print("Mean diff between f06 and f25:", diff.mean(axis=(0,1)))

print("img25 center:", img25[h//2, w//2])
print("img25 top-left:", img25[200, 200])
print("img25 bot-right:", img25[800, 1600])

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\thumb_f25.jpg", cv2.resize(img25, (960, 540)))

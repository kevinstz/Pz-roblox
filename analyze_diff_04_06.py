import cv2
import numpy as np

img04 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f04.jpg")
img06 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f06.jpg")

diff = cv2.absdiff(img04, img06)
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
mask = (gray > 25).astype(np.uint8) * 255

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\diff_04_06_vis.jpg", diff * 3)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\diff_04_06_mask.png", mask)

# Let's find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Total diff contours between f04 and f06: {len(contours)}")

# Areas
areas = sorted([(cv2.contourArea(c), cv2.boundingRect(c)) for c in contours], key=lambda x: x[0], reverse=True)
for i in range(min(10, len(areas))):
    print(f"#{i}: area={areas[i][0]:.0f}, rect={areas[i][1]}")

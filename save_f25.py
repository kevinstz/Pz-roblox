import cv2
import os

d = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\video3_5fps"
img25 = cv2.imread(os.path.join(d, "f_025_4.58s.jpg"))
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f25.jpg", img25)

# Also let's inspect f_004 (which is MISSING) and f_006 (which is RENDERED)
img04 = cv2.imread(os.path.join(d, "f_004_0.73s.jpg"))
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f04.jpg", img04)

img06 = cv2.imread(os.path.join(d, "f_006_1.10s.jpg"))
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f06.jpg", img06)

print("Saved full_f25, full_f04, full_f06.")

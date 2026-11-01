import cv2

img04 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f04.jpg")
img06 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_f06.jpg")

# Contour #1: (1061, 591, 444, 153)
c1_04 = img04[591:591+153, 1061:1061+444]
c1_06 = img06[591:591+153, 1061:1061+444]

cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\c1_04.jpg", c1_04)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\c1_06.jpg", c1_06)

# What is c1?
print("c1_04 mean BGR:", c1_04.mean(axis=(0,1)))
print("c1_06 mean BGR:", c1_06.mean(axis=(0,1)))

import cv2

vp10 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp10_full.jpg")

# 1. Park curb on left: y: 200..600, x: 0..400
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_park_curb.jpg", vp10[200:600, 0:400])

# 2. Sidewalk across the street: y: 0..300, x: 300..1000
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_street_crossing.jpg", vp10[0:300, 300:1000])

# 3. Grass bottom right: y: 400..740, x: 800..1500
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_grass_fence.jpg", vp10[400:740, 800:1500])

# 4. Curb right above player: y: 150..400, x: 600..1100
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_curb_crossing.jpg", vp10[150:400, 600:1100])

print("Saved crop10 images.")

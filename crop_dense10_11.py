import cv2
import numpy as np

p = r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg'
img = cv2.imread(p)

# Player is at approx (964, 661). Let's crop 400x400 around player:
crop_player = img[max(0, 661-200):min(1080, 661+200), max(0, 964-200):min(1920, 964+200)]
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_player_dense10.jpg', crop_player)

# Also let's crop the top-middle area where the flickering happens:
# y from 160 to 360, x from 500 to 1400:
crop_flicker10 = img[160:360, 500:1400]
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_flicker_dense10.jpg', crop_flicker10)

img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')
crop_flicker11 = img11[160:360, 500:1400]
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_flicker_dense11.jpg', crop_flicker11)

print("Saved crops successfully.")

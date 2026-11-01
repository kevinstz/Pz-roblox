import cv2

img = cv2.imread(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop_frame15.jpg')
h, w, _ = img.shape
print("crop_frame15 shape:", h, w)
print("mean BGR:", img.mean(axis=(0,1)))

# Let's inspect subregions of crop_frame15:
print("top 100:", img[:100, :].mean(axis=(0,1)))
print("mid 100:", img[250:350, :].mean(axis=(0,1)))
print("bot 100:", img[-100:, :].mean(axis=(0,1)))

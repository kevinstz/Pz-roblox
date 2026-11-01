import cv2

img = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
top_strip = img[0:180, :]
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\top_strip.jpg', top_strip)
print(f"Top strip shape: {top_strip.shape}")

# Also let's check what is at y=0..167 in img:
# Is it the Roblox Studio window title bar / ribbon / menu?
# Let's sample colors across rows 0..170:
for y in range(0, 180, 20):
    print(f"row y={y}: mean BGR = {img[y, :].mean(axis=0)}")

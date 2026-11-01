import cv2

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')

crop10 = img10[150:350, 600:1000]
crop11 = img11[150:350, 600:1000]

cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop10_inspect_area.jpg', crop10)
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\crop11_inspect_area.jpg', crop11)

print("Saved crop10 and crop11 successfully.")

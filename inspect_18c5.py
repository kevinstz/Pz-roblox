import cv2

img = cv2.imread(r"out\textures\18c5e13465b6791a2b61.png", cv2.IMREAD_UNCHANGED)
print("18c5 shape:", img.shape)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\tex_18c5.png", img)
print("Saved tex_18c5.png")

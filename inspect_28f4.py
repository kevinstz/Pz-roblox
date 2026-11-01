import cv2

img = cv2.imread(r"out\textures\28f483ee7d0736992bde.png", cv2.IMREAD_UNCHANGED)
print("28f4 shape:", img.shape)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\tex_28f4.png", img)
print("Saved tex_28f4.png")

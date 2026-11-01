import cv2

img = cv2.imread(r"out\textures\334d48f51be74b5e9e1a.png", cv2.IMREAD_UNCHANGED)
print("334d shape:", img.shape)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\tex_334d.png", img)
print("Saved tex_334d.png")

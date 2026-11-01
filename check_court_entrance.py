import cv2

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_court_entrance.jpg")
print("court entrance shape:", img.shape)
# Compare with Rosewood_Downtown_Reference.png at court entrance
ref = cv2.imread(r"out\Rosewood_Downtown_Reference.png")
print("ref shape:", ref.shape)

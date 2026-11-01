import cv2

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_008_3.87s.jpg")
h, w, _ = img.shape
print("Frame shape:", h, w)

# Let's crop:
# 1. Top left building (behind fence)
cv2.imwrite("v4_crop_top_left.jpg", img[0:int(h*0.45), 0:int(w*0.45)])
# 2. Top center/right building (across street)
cv2.imwrite("v4_crop_top_right.jpg", img[0:int(h*0.45), int(w*0.45):w])
# 3. Bottom left building (closest foreground building with the roof and floating object)
cv2.imwrite("v4_crop_bot_left.jpg", img[int(h*0.45):h, 0:int(w*0.45)])
# 4. Bottom right
cv2.imwrite("v4_crop_bot_right.jpg", img[int(h*0.45):h, int(w*0.45):w])

print("Crops saved successfully.")

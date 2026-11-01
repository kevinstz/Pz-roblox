import cv2

img6 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_006_2.90s.jpg")
crop_white2 = img6[750:950, 450:700]
cv2.imwrite("white_obj_crop2.jpg", crop_white2)
print("Saved white_obj_crop2.jpg")

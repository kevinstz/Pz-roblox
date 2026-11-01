import cv2

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_006_2.90s.jpg")

# Front corner of left building with white box/door frame
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_front_corner_door.jpg", img[550:900, 280:480])

# Upper parapet and corner of left building
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_corner_parapet.jpg", img[350:700, 250:500])

print("Saved!")

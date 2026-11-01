import cv2

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_006_2.90s.jpg")
h, w, _ = img.shape

# 1. Lower left roof
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_lower_left_roof.jpg", img[600:1000, 0:500])

# 2. Left building upper wall panels and white frame
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_wall_panels.jpg", img[250:900, 0:600])

# 3. Across street building (windows with sticks/lines)
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_court_windows.jpg", img[150:400, 800:1300])

# 4. Across street building entrance & roofline
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_court_entrance.jpg", img[150:550, 1100:1600])

print("Crops saved!")

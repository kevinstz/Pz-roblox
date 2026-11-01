import cv2

img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_008_3.87s.jpg")
h, w, _ = img.shape

# The lower-left roof is at y = 0.55*h .. 0.9*h, x = 0 .. 0.25*w
roof_crop = img[int(h*0.55):int(h*0.88), 0:int(w*0.25)]
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_lower_left_roof_zoom.jpg", roof_crop)
print("Saved zoom crop.")

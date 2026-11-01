import cv2

img = cv2.imread('ref_target_bld.jpg')
h, w, _ = img.shape
# Save top half and bottom half
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_top.jpg", img[:int(h*0.5), :])
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_bottom.jpg", img[int(h*0.5):, :])
print("Saved ref_top and ref_bottom")

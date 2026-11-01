import cv2

img = cv2.imread("out/Rosewood_Downtown_Reference.png")
h, w, _ = img.shape
# Save 4 quadrants
cv2.imwrite("ref_top_left.jpg", img[0:h//2, 0:w//2])
cv2.imwrite("ref_top_right.jpg", img[0:h//2, w//2:w])
cv2.imwrite("ref_bot_left.jpg", img[h//2:h, 0:w//2])
cv2.imwrite("ref_bot_right.jpg", img[h//2:h, w//2:w])
print("Saved reference quadrants!")

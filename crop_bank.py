import cv2

img = cv2.imread("ref_top_right.jpg")
# Knox bank is in the middle of ref_top_right.jpg
# Let's crop Knox bank
h, w, _ = img.shape
crop_bank = img[int(h*0.3):int(h*0.8), int(w*0.1):int(w*0.5)]
cv2.imwrite("ref_knox_bank.jpg", crop_bank)
print("Saved ref_knox_bank.jpg")

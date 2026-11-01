import cv2

img = cv2.imread("out/Rosewood_Downtown_Reference.png")
# Knox Bank and the market/bar across street:
# In ref_top_right, Knox bank is around y in [200, 600], x in [1200, 1800]
# The building with flat roof is around y in [700, 1100], x in [1400, 2000]
crop_bld = img[600:1270, 1300:2200]
cv2.imwrite("ref_target_bld.jpg", crop_bld)
print("Saved ref_target_bld.jpg")

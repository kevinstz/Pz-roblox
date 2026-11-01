import cv2

ref = cv2.imread(r"out\Rosewood_Downtown_Reference.png")
h, w, _ = ref.shape

# Knox Bank is around center-left in ref_q_tr.
# In full reference, ref_q_tr is x: 1200..2400, y: 0..638
# Let's crop the supermarket / bar building:
# Knox bank is around x: 1400..1800, y: 300..600
# The supermarket is to the lower-left or left of Knox bank:
supermarket_crop = ref[500:1000, 1100:1800]
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_supermarket.jpg", supermarket_crop)
print("Saved ref_supermarket.jpg")

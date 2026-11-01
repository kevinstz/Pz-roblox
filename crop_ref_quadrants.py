import cv2

ref = cv2.imread(r"out\Rosewood_Downtown_Reference.png")
h, w, _ = ref.shape
print(f"Reference shape: {w}x{h}")

# In Rosewood_Downtown_Reference.png, where is Bar_31_45_12 / grocery store?
# Let's save crops of the grocery / bar building from the reference image
# Downtown Rosewood reference:
# Usually parking lot is in the center/left
# Let's save 4 quadrants of the reference map to locate the building exactly
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_q_tl.jpg", ref[0:h//2, 0:w//2])
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_q_tr.jpg", ref[0:h//2, w//2:w])
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_q_bl.jpg", ref[h//2:h, 0:w//2])
cv2.imwrite(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_q_br.jpg", ref[h//2:h, w//2:w])
print("Saved reference quadrants.")

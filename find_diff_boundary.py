import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')

diff = cv2.absdiff(img10, img11)
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
mask = (gray > 30).astype(np.uint8) * 255

# Let's find contours of the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Found {len(contours)} diff contours")

# Sort contours by area
areas = [(cv2.contourArea(c), c) for c in contours]
areas.sort(key=lambda x: x[0], reverse=True)

for i in range(min(5, len(areas))):
    area, c = areas[i]
    x, y, w, h = cv2.boundingRect(c)
    print(f"Contour #{i}: area={area:.0f}, rect=(x={x}, y={y}, w={w}, h={h})")

# Let's create an image showing the contour outline on img10
overlay = img10.copy()
cv2.drawContours(overlay, [areas[0][1]], -1, (0, 0, 255), 3)
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\diff_contour_overlay.jpg', overlay)
print("Saved diff_contour_overlay.jpg")

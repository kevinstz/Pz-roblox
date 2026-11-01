import cv2
import numpy as np

img = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')
h, w, _ = img.shape

# In dense_11, find where the green starts along each vertical column x
# Green has HSV: H between 35 and 85, S > 50, V between 50 and 200
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# TerrenoCircundante green color
# BGR is around (36, 86, 68) -> HSV: H=70, S=148, V=86
green_mask = cv2.inRange(hsv, (50, 80, 50), (85, 255, 150))

# For columns x from 200 to 1700, find the lowest Y that is green in the upper screen
boundary_y = []
cols = list(range(200, 1700, 20))
for x in cols:
    # Look from y=100 down to y=800
    col = green_mask[100:800, x]
    # Find transitions or contiguous green blocks
    # Where is it green?
    green_ys = np.where(col > 0)[0] + 100
    if len(green_ys) > 0:
        boundary_y.append(green_ys.max())
    else:
        boundary_y.append(-1)

for x, by in zip(cols, boundary_y):
    print(f"col x={x:4d}: max green y = {by}")

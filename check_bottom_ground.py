import cv2
import numpy as np

img10 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
img11 = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_11_3.12s.jpg')

# Let's check ground around the player / bottom of the screen:
# y = 600..800, x = 400..1200
crop_bot10 = img10[600:800, 400:1200]
crop_bot11 = img11[600:800, 400:1200]

diff_bot = cv2.absdiff(crop_bot10, crop_bot11)
print("Mean diff at bottom (B, G, R):", diff_bot.mean(axis=(0,1)))

# Let's sample pavement at the bottom in crop_bot10 and crop_bot11:
for y in [50, 100, 150]:
    for x in [100, 300, 500, 700]:
        print(f"bottom (y={y}, x={x}): crop10={crop_bot10[y, x]}, crop11={crop_bot11[y, x]}")

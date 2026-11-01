import cv2
import os

frames_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames"
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

img = cv2.imread(os.path.join(frames_dir, "frame_002_1.97s.jpg"))
# Viewport in Roblox Studio is approximately:
# x: 0 to 1500, y: 150 to 890
viewport = img[150:890, 0:1500]
cv2.imwrite(os.path.join(out_dir, "crop_viewport_f2.jpg"), viewport)

# Let's also crop top-center, middle-left, center, bottom-right
cv2.imwrite(os.path.join(out_dir, "crop_top_center.jpg"), viewport[0:400, 400:1100])
cv2.imwrite(os.path.join(out_dir, "crop_center_player.jpg"), viewport[200:600, 500:900])
cv2.imwrite(os.path.join(out_dir, "crop_left_park.jpg"), viewport[100:600, 0:500])
cv2.imwrite(os.path.join(out_dir, "crop_bottom_right.jpg"), viewport[400:740, 700:1500])

print("Saved crops successfully.")

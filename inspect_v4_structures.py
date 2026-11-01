import cv2
import numpy as np

# Let's inspect v4_crop_top_right and v4_crop_top_left and v4_crop_bot_left
# We can save small detailed slices to understand what's visible!
img = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video4_frames\frame_008_3.87s.jpg")
h, w, _ = img.shape

# Let's check:
# 1. Top building roof (across the street)
top_roof = img[0:int(h*0.35), int(w*0.35):int(w*0.85)]
cv2.imwrite("dbg_top_roof.jpg", top_roof)

# 2. Left side building (behind fence or next to it)
left_bld = img[int(h*0.1):int(h*0.5), 0:int(w*0.4)]
cv2.imwrite("dbg_left_bld.jpg", left_bld)

# 3. Parapet wall and roofs of Bar / foreground building
bot_left = img[int(h*0.4):int(h*0.95), 0:int(w*0.5)]
cv2.imwrite("dbg_bot_left.jpg", bot_left)

print("Saved dbg crops.")

import cv2
import numpy as np

# In dense_10_2.83s.jpg, what landmarks are near the player?
# Let's check what buildings/objects are near the player
# Let's crop the scene around the player and inspect landmark colors/features
img = cv2.imread(r'C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video3_frames_dense\dense_10_2.83s.jpg')
# Let's save a view of the full frame with grid lines
cv2.imwrite(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\full_10_labeled.jpg', img)

# Let's check player world position:
# In the previous session, the player was in Rosewood.
# Where in Rosewood? Near the Police Station or Court or Clinic?

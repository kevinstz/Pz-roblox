import cv2
import numpy as np

v2 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp_02.jpg")
v6 = cv2.imread(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\vp_06.jpg")

# In v2, row 0 to 180 is green terrain
# In v6, row 0 to 180 is road, curbs, buildings!
# Let's see what row 180 onwards looks like:
diff_bottom = np.abs(v2[200:, :].astype(float) - v6[200:, :].astype(float)).mean()
print(f"Mean pixel diff in bottom half (rows 200..end): {diff_bottom:.2f}")

diff_top = np.abs(v2[:150, :].astype(float) - v6[:150, :].astype(float)).mean()
print(f"Mean pixel diff in top half (rows 0..150): {diff_top:.2f}")

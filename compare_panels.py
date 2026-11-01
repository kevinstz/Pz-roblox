import cv2
import numpy as np

ref_top = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\ref_top.jpg")
panels = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\crop_v4_wall_panels.jpg")

print("Ref top shape:", ref_top.shape)
print("Panels crop shape:", panels.shape)

# Let's see: in panels crop, where are the light cyan/grey patches?
# Light cyan/grey patches in panels crop have high G and B compared to brown brick
is_cyan = (panels[:,:,0] > 90) & (panels[:,:,1] > 90) & (panels[:,:,2] < 120) & (panels[:,:,1] > panels[:,:,2] - 10)
print("Cyan pixels in panels crop:", np.sum(is_cyan))

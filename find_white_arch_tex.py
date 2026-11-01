import os
import cv2
import numpy as np

# Load white_obj_v4
query = cv2.imread(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\white_obj_v4.jpg")
qh, qw, _ = query.shape

tex_dir = r"out\textures"
files = [f for f in os.listdir(tex_dir) if f.endswith('.png')]
print(f"Searching through {len(files)} textures...")

matches = []
for f in files:
    p = os.path.join(tex_dir, f)
    img = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if img is None:
        continue
    # We want textures that have white/light pixels (>200) and an arched shape or significant size
    # Check if shape is tall (like a door or window: h > 100)
    h, w = img.shape[:2]
    if h >= 80 and w >= 40:
        # Check white content
        if len(img.shape) == 3 or (len(img.shape) == 4 and np.max(img[:,:,3]) > 0):
            rgb = img[:,:,:3] if len(img.shape) >= 3 else img
            # Average brightness of non-transparent pixels
            if len(img.shape) == 4:
                mask = img[:,:,3] > 100
                if np.sum(mask) > 100:
                    bright = np.mean(rgb[mask])
                    if bright > 160: # light colored
                        matches.append((f, bright, (h, w)))
            else:
                bright = np.mean(rgb)
                if bright > 160:
                    matches.append((f, bright, (h, w)))

print(f"Found {len(matches)} bright tall textures.")
matches.sort(key=lambda x: x[1], reverse=True)
for m in matches[:30]:
    print(f"{m[0]}: brightness={m[1]:.1f}, size={m[2]}")

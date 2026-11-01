from PIL import Image
import os

frames_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video2_frames_dense"
out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

im = Image.open(os.path.join(frames_dir, "dense_04_1.93s.jpg"))
# Crop center, top left, top right, bottom left, bottom right
w, h = im.size

# Let's save a reduced version of dense_04 for inspection
im_thumb = im.resize((960, 540))
im_thumb.save(os.path.join(out_dir, "video_frame4_thumb.jpg"))
print("Saved video_frame4_thumb.jpg")

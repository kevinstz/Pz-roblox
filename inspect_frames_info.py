import os
from PIL import Image

frames_dir = r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\video2_frames_dense"
files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])

print(f"Total dense frames: {len(files)}")
for f in files:
    p = os.path.join(frames_dir, f)
    im = Image.open(p)
    print(f"  {f}: size={im.size}, mode={im.mode}")

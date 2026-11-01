from PIL import Image
import numpy as np

im = Image.open(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\dbg_composite_corner.png")
# Downsample to 40x40
thumb = im.resize((40, 40), Image.BILINEAR)
arr = np.array(thumb)
# Curb is light grey / white, sidewalk is medium, road is dark
# Let's see grayscale
lum = arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114

lines = []
for r in range(40):
    row = ""
    for c in range(40):
        v = lum[r, c]
        if v > 150:
            row += "#"
        elif v > 120:
            row += "+"
        elif v > 80:
            row += "."
        elif v > 0:
            row += " "
        else:
            row += " "
    lines.append(row)

print("Composite 2D corner preview (40x40):")
print("\n".join(lines))

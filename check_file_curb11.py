from PIL import Image
import numpy as np

p = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures\969234b5beed7cdc6e68.png"
im = Image.open(p)
arr = np.array(im)
print("Shape:", arr.shape)
alpha = arr[:, :, 3]
print("Alpha mean:", alpha.mean())

def ascii_art(arr, w=24, h=24):
    im = Image.fromarray(arr).resize((w, h), Image.BILINEAR)
    data = np.array(im)
    out = []
    for r in range(h):
        line = ""
        for c in range(w):
            val = data[r, c]
            if val > 150:
                line += "#"
            elif val > 50:
                line += "."
            else:
                line += " "
        out.append(line)
    return "\n".join(out)

print(ascii_art(alpha))

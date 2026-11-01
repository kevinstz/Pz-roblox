from PIL import Image
import numpy as np

def ascii_art(arr, w=20, h=10):
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

for h in ['f8a808a3e99a2210a132', 'd400dbc4c15891a01895', 'ce9c3faca880178fb24b']:
    p = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\out\\textures\\{h}.png"
    im = Image.open(p)
    alpha = np.array(im)[:, :, 3]
    print(f"=== {h} alpha_mean={alpha.mean():.1f} ===")
    print(ascii_art(alpha, 20, 10))

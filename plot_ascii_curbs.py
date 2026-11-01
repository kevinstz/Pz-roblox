from PIL import Image
import numpy as np

def ascii_art(arr, w=32, h=16):
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

for i in [0, 4, 5, 8, 9]:
    p_raw = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_raw_street_curbs_01_{i}.png"
    p_unp = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_unproj_street_curbs_01_{i}.png"
    im_raw = Image.open(p_raw)
    im_unp = Image.open(p_unp)
    arr_raw = np.array(im_raw)[:, :, 3]
    arr_unp = np.array(im_unp)[:, :, 3]
    print(f"=== Raw Curb {i} (in 128x256 sprite, showing diamond y=192..256) ===")
    print(ascii_art(arr_raw[192:256, :], 32, 16))
    print(f"=== Current Unprojected Curb {i} (128x128 square) ===")
    print(ascii_art(arr_unp, 24, 24))
    print("=" * 50)

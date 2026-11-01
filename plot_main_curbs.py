from PIL import Image
import numpy as np

def ascii_art(arr, w=24, h=16):
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

for i in [8, 9, 10, 11, 40, 41, 42, 43]:
    p_raw = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_raw_street_curbs_01_{i}.png"
    p_unp = f"C:\\Users\\julia\\.gemini\\antigravity\\scratch\\pz_roblox_b42\\dbg_unproj_street_curbs_01_{i}.png"
    try:
        im_raw = Image.open(p_raw)
        im_unp = Image.open(p_unp)
        arr_raw = np.array(im_raw)[:, :, 3]
        arr_unp = np.array(im_unp)[:, :, 3]
        print(f"=== Curb {i} Raw Diamond ===")
        print(ascii_art(arr_raw[192:256, :], 24, 12))
        print(f"=== Curb {i} Unprojected ===")
        print(ascii_art(arr_unp, 20, 20))
    except Exception as e:
        print(f"Curb {i}: {e}")
    print("=" * 40)

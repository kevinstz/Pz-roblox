from PIL import Image
import os

out_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42"

# Inspect dbg_unproj_street_curbs_01_1.png and dbg_raw_street_curbs_01_1.png
im_raw = Image.open(os.path.join(out_dir, "dbg_raw_street_curbs_01_1.png"))
im_unp = Image.open(os.path.join(out_dir, "dbg_unproj_street_curbs_01_1.png"))
print("Raw curb 1 size:", im_raw.size, "bbox:", im_raw.getbbox())
print("Unproj curb 1 size:", im_unp.size, "bbox:", im_unp.getbbox())

im_raw4 = Image.open(os.path.join(out_dir, "dbg_raw_street_curbs_01_4.png"))
im_unp4 = Image.open(os.path.join(out_dir, "dbg_unproj_street_curbs_01_4.png"))
print("Raw curb 4 size:", im_raw4.size, "bbox:", im_raw4.getbbox())
print("Unproj curb 4 size:", im_unp4.size, "bbox:", im_unp4.getbbox())

from PIL import Image

im = Image.open(r"C:\Users\julia\.gemini\antigravity\brain\83b1d910-8a99-4008-af1c-53cbcbfd7d30\.user_uploaded\media_1793236645461_9e7811ab.png")
print("Size of screenshot 6:", im.size)

# Crop the corner curb area
w, h = im.size
crop1 = im.crop((int(w * 0.4), int(h * 0.2), int(w * 0.8), int(h * 0.8)))
crop1.save(r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\dbg_crop_curb6.png")
print("Saved dbg_crop_curb6.png")

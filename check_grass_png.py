from PIL import Image

img_path = r"C:\Users\julia\AppData\Local\Roblox\Versions\version-7062aec9dbe74b14\content\pz42\2ff459223cdeb182054f.png"
im = Image.open(img_path)
print("Size:", im.size)
print("BBox:", im.getbbox())
ext = im.getextrema()
print("Extrema:", ext)

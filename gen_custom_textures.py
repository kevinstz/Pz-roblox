import os
import hashlib
from PIL import Image, ImageDraw

tex_dir = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"
os.makedirs(tex_dir, exist_ok=True)

def put_texture(img):
    import io
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    data = buf.getvalue()
    h = hashlib.sha1(data).hexdigest()[:20]
    p = os.path.join(tex_dir, h + '.png')
    with open(p, 'wb') as f:
        f.write(data)
    url = f"rbxasset://pz42/{h}.png"
    return url, h

# 1. Dark Corrugated Metal Roof (roofs_01)
# Dimensions 256x256, vertical corrugated ribs with highlights and shadows
im_roof_dark = Image.new("RGBA", (256, 256), (48, 52, 58, 255))
d = ImageDraw.Draw(im_roof_dark)
for x in range(0, 256, 16):
    # Rib shadow and highlight
    d.line([(x, 0), (x, 255)], fill=(30, 32, 36, 255), width=3)
    d.line([(x+3, 0), (x+3, 255)], fill=(75, 82, 90, 255), width=2)
    d.line([(x+5, 0), (x+5, 255)], fill=(55, 60, 66, 255), width=8)
    d.line([(x+13, 0), (x+13, 255)], fill=(38, 42, 46, 255), width=3)
# Horizontal sheet seam lines every 64 pixels
for y in range(0, 256, 64):
    d.line([(0, y), (255, y)], fill=(25, 27, 30, 255), width=2)
    d.line([(0, y+1), (255, y+1)], fill=(85, 92, 100, 255), width=1)
url_roof_dark, h_roof_dark = put_texture(im_roof_dark)

# 2. Tan / Earthy Corrugated Roof (roofs_02)
im_roof_tan = Image.new("RGBA", (256, 256), (145, 125, 100, 255))
d = ImageDraw.Draw(im_roof_tan)
for x in range(0, 256, 16):
    d.line([(x, 0), (x, 255)], fill=(105, 90, 70, 255), width=3)
    d.line([(x+3, 0), (x+3, 255)], fill=(185, 165, 135, 255), width=2)
    d.line([(x+5, 0), (x+5, 255)], fill=(155, 135, 110, 255), width=8)
    d.line([(x+13, 0), (x+13, 255)], fill=(115, 100, 80, 255), width=3)
for y in range(0, 256, 64):
    d.line([(0, y), (255, y)], fill=(95, 80, 60, 255), width=2)
    d.line([(0, y+1), (255, y+1)], fill=(195, 175, 145, 255), width=1)
url_roof_tan, h_roof_tan = put_texture(im_roof_tan)

# 3. Horizontal Vinyl / Clapboard Siding (siding)
im_siding = Image.new("RGBA", (256, 256), (255, 255, 255, 255))
d = ImageDraw.Draw(im_siding)
for y in range(0, 256, 16):
    # Bottom lap shadow
    d.line([(0, y), (255, y)], fill=(180, 180, 185, 255), width=2)
    d.line([(0, y+1), (255, y+1)], fill=(255, 255, 255, 255), width=1)
    # Subtle gradient
    for dy in range(2, 16):
        c = 240 + int(dy * 1.0)
        d.line([(0, y+dy), (255, y+dy)], fill=(c, c, c, 255), width=1)
url_siding, h_siding = put_texture(im_siding)

# 4. Foundation Cinderblock Skirting (skirting)
im_skirt = Image.new("RGBA", (256, 256), (130, 132, 135, 255))
d = ImageDraw.Draw(im_skirt)
for row in range(0, 256, 32):
    # Mortar line
    d.line([(0, row), (255, row)], fill=(85, 85, 88, 255), width=3)
    d.line([(0, row+3), (255, row+3)], fill=(160, 162, 165, 255), width=1)
    # Staggered vertical blocks
    offset = 32 if (row // 32) % 2 == 1 else 0
    for col in range(offset, 256 + 64, 64):
        d.line([(col, row+3), (col, row+31)], fill=(85, 85, 88, 255), width=3)
url_skirt, h_skirt = put_texture(im_skirt)

# 5. Wood Deck Planks (porch)
im_wood = Image.new("RGBA", (256, 256), (135, 95, 60, 255))
d = ImageDraw.Draw(im_wood)
for x in range(0, 256, 24):
    d.line([(x, 0), (x, 255)], fill=(80, 55, 35, 255), width=2)
    d.line([(x+1, 0), (x+1, 255)], fill=(165, 120, 80, 255), width=1)
url_wood, h_wood = put_texture(im_wood)

# 6. Window AC Unit Grill
im_ac = Image.new("RGBA", (128, 128), (220, 222, 225, 255))
d = ImageDraw.Draw(im_ac)
d.rectangle([(8, 8), (119, 119)], fill=(200, 202, 205, 255), outline=(120, 122, 125, 255), width=2)
# Louver slats
for y in range(16, 110, 6):
    d.line([(16, y), (90, y)], fill=(40, 42, 45, 255), width=2)
    d.line([(16, y+2), (90, y+2)], fill=(160, 162, 165, 255), width=1)
# Controls panel on right
d.rectangle([(96, 20), (112, 105)], fill=(70, 72, 75, 255))
d.ellipse([(100, 30), (108, 38)], fill=(180, 185, 190, 255))
d.ellipse([(100, 50), (108, 58)], fill=(180, 185, 190, 255))
url_ac, h_ac = put_texture(im_ac)

print("Created and registered 6 custom high-fidelity textures:")
print("  Dark Roof:", url_roof_dark)
print("  Tan Roof: ", url_roof_tan)
print("  Siding:   ", url_siding)
print("  Skirting: ", url_skirt)
print("  Wood Deck:", url_wood)
print("  AC Unit:  ", url_ac)

import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pos = content.find("CAMERA_DISTANCE")
while pos != -1:
    # Look back for <Item
    item_start = content.rfind("<Item", 0, pos)
    props_end = content.find("</Properties>", item_start)
    print("Found CAMERA_DISTANCE at pos:", pos)
    print("Item header:")
    print(content[item_start:props_end+13])
    pos = content.find("CAMERA_DISTANCE", pos + 1)

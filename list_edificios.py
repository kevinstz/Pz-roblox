import xml.etree.ElementTree as ET

# Instead of full XML parse which takes 400MB RAM, let's parse Edificios cleanly
rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

buildings = []
inside_edificios = False
current_bldg = None
bldg_depth = 0

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<Item class="Folder"' in line:
            pass
        if '<string name="Name">Edificios</string>' in line:
            inside_edificios = True
            continue
        if inside_edificios:
            if '<Item class="Model"' in line:
                bldg_depth += 1
            elif '</Item>' in line:
                bldg_depth -= 1
                if bldg_depth == 0:
                    current_bldg = None
                elif bldg_depth < 0:
                    # Exited Edificios folder
                    break
            
            if bldg_depth == 1 and '<string name="Name">' in line:
                name = line.split('<string name="Name">')[1].split('</string>')[0]
                buildings.append(name)

print(f"Total Buildings in Edificios: {len(buildings)}")
for b in buildings:
    print(" -", b)

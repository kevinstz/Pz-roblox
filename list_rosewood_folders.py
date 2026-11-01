rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_rosewood = False
    depth = 0
    items = []
    for line in f:
        if 'name="Name">PZ_Rosewood_B42<' in line:
            in_rosewood = True
            depth = 1
            continue
        if in_rosewood:
            if '<Item' in line:
                depth += 1
                if depth == 2:
                    items.append([line.strip()])
            elif '</Item>' in line:
                depth -= 1
                if depth == 0:
                    break
            elif depth == 2 and items:
                if '<string name="Name">' in line:
                    items[-1].append(line.strip())

for it in items:
    print(it)

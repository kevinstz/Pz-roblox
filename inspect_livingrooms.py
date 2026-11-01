import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def inspect_building(target_name):
    print(f"=== Inspecting {target_name} ===")
    inside = False
    depth = 0
    parts = []
    
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        curr_part = None
        for line in f:
            if '<Item class="Model"' in line:
                depth += 1
            elif '</Item>' in line:
                if curr_part and '<Item class="Part"' in curr_part.get("open", ""):
                    # closing a part
                    parts.append(curr_part)
                    curr_part = None
                depth -= 1
                if inside and depth == 0:
                    break
            
            if not inside:
                if f'<string name="Name">{target_name}</string>' in line:
                    inside = True
                    depth = 1
                continue
            
            # Inside the target building
            if '<Item class="Part"' in line:
                curr_part = {"open": line, "name": "", "pos": None, "size": None, "textures": []}
            elif curr_part:
                if '<string name="Name">' in line:
                    curr_part["name"] = line.split('<string name="Name">')[1].split('</string>')[0]
                elif '<string name="Texture">' in line:
                    curr_part["textures"].append(line.split('<string name="Texture">')[1].split('</string>')[0])
                elif '<X>' in line and '<Y>' in line and '<Z>' in line:
                    mx = re.search(r'<X>([-\d\.]+)</X>', line)
                    my = re.search(r'<Y>([-\d\.]+)</Y>', line)
                    mz = re.search(r'<Z>([-\d\.]+)</Z>', line)
                    if mx and my and mz:
                        vec = (float(mx.group(1)), float(my.group(1)), float(mz.group(1)))
                        if curr_part["pos"] is None:
                            curr_part["pos"] = vec
                        elif curr_part["size"] is None:
                            curr_part["size"] = vec

    print(f"Total parts in {target_name}: {len(parts)}")
    xs = [p["pos"][0] for p in parts if p["pos"]]
    ys = [p["pos"][1] for p in parts if p["pos"]]
    zs = [p["pos"][2] for p in parts if p["pos"]]
    if xs:
        print(f"X range: {min(xs):.2f} to {max(xs):.2f} (span: {max(xs)-min(xs):.2f})")
        print(f"Y range: {min(ys):.2f} to {max(ys):.2f} (span: {max(ys)-min(ys):.2f})")
        print(f"Z range: {min(zs):.2f} to {max(zs):.2f} (span: {max(zs)-min(zs):.2f})")
    
    # Types of parts
    part_types = {}
    for p in parts:
        prefix = p["name"].split('_')[0] if '_' in p["name"] else p["name"].split('|')[0]
        part_types[prefix] = part_types.get(prefix, 0) + 1
    print("Part types summary:", part_types)
    
    # Wall textures
    wall_tex = set()
    for p in parts:
        if 'wall' in p["name"].lower() or any('wall' in t.lower() for t in p["textures"]):
            for t in p["textures"]:
                wall_tex.add(t.split('/')[-1])
            wall_tex.add(p["name"])
    print("Wall items / textures (sample):", list(wall_tex)[:15])
    return parts

parts_28 = inspect_building("Livingroom_31_45_28")
parts_33 = inspect_building("Livingroom_31_45_33")

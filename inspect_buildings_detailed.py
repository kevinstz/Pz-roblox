import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# We want to inspect each building under Edificios
# Gather: Name, floors, part count, bounding box of parts (min/max X, Y, Z), sample textures/wall names

building_data = {}
current_building = None
current_floor = None
stack = []

def parse_vector3(line):
    # <X>...</X><Y>...</Y><Z>...</Z>
    mx = re.search(r'<X>([-\d\.]+)</X>', line)
    my = re.search(r'<Y>([-\d\.]+)</Y>', line)
    mz = re.search(r'<Z>([-\d\.]+)</Z>', line)
    if mx and my and mz:
        return float(mx.group(1)), float(my.group(1)), float(mz.group(1))
    return None

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)"', line)
        if m_item:
            stack.append({"class": m_item.group(1), "name": None, "pos": None, "size": None})
            continue
            
        m_name = re.search(r'<string name="Name">(.*?)</string>', line)
        if m_name and stack:
            if stack[-1]["name"] is None:
                name = m_name.group(1)
                stack[-1]["name"] = name
                # Check if this is a direct child of Edificios
                if len(stack) >= 2 and stack[-2].get("name") == "Edificios":
                    current_building = name
                    building_data[current_building] = {
                        "floors": set(),
                        "parts": 0,
                        "min_x": 1e9, "max_x": -1e9,
                        "min_y": 1e9, "max_y": -1e9,
                        "min_z": 1e9, "max_z": -1e9,
                        "wall_textures": set(),
                    }
                elif current_building and len(stack) >= 3 and stack[-3].get("name") == "Edificios":
                    if name.startswith("Piso_"):
                        building_data[current_building]["floors"].add(name)

        if current_building and stack and stack[-1]["class"] in ["Part", "WedgePart"]:
            # Check CFrame and Size
            if '<X>' in line and '<Y>' in line and '<Z>' in line:
                vec = parse_vector3(line)
                if vec:
                    if stack[-1]["pos"] is None:
                        stack[-1]["pos"] = vec
                    elif stack[-1]["size"] is None:
                        stack[-1]["size"] = vec

        if '<string name="Texture">' in line and current_building:
            m_tex = re.search(r'<string name="Texture">(.*?)</string>', line)
            if m_tex:
                tex = m_tex.group(1)
                if 'wall' in tex or 'siding' in tex or 'roof' in tex:
                    building_data[current_building]["wall_textures"].add(tex.split('/')[-1])

        if '</Item>' in line:
            if stack:
                popped = stack.pop()
                if popped.get("name") == "Edificios":
                    current_building = None
                    break
                if current_building and popped.get("class") in ["Part", "WedgePart"]:
                    if popped.get("pos"):
                        px, py, pz = popped["pos"]
                        sx, sy, sz = popped.get("size", (0, 0, 0))
                        b = building_data[current_building]
                        b["parts"] += 1
                        b["min_x"] = min(b["min_x"], px - sx/2)
                        b["max_x"] = max(b["max_x"], px + sx/2)
                        b["min_y"] = min(b["min_y"], py - sy/2)
                        b["max_y"] = max(b["max_y"], py + sy/2)
                        b["min_z"] = min(b["min_z"], pz - sz/2)
                        b["max_z"] = max(b["max_z"], pz + sz/2)

print(f"{'Building Name':<30} | {'Floors':<20} | {'Parts':<6} | {'Bounds (X, Z)':<35} | {'Height (Y)'}")
print("-" * 110)
for name, data in building_data.items():
    floors_str = ", ".join(sorted(data["floors"]))
    dx = data["max_x"] - data["min_x"]
    dz = data["max_z"] - data["min_z"]
    dy = data["max_y"] - data["min_y"]
    bounds = f"X:[{data['min_x']:.1f}..{data['max_x']:.1f}]({dx:.1f}) Z:[{data['min_z']:.1f}..{data['max_z']:.1f}]({dz:.1f})"
    y_str = f"[{data['min_y']:.1f}..{data['max_y']:.1f}]({dy:.1f})"
    print(f"{name:<30} | {floors_str:<20} | {data['parts']:<6} | {bounds:<35} | {y_str}")

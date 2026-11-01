import xml.etree.ElementTree as ET

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def inspect_house_detailed(target_name):
    print(f"\n==========================================")
    print(f"DETAILED INSPECTION: {target_name}")
    print(f"==========================================")
    
    inside = False
    open_items = 0
    captured_lines = []
    
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        prev_lines = []
        for line in f:
            if not inside:
                if f'<string name="Name">{target_name}</string>' in line:
                    inside = True
                    models = [i for i, l in enumerate(prev_lines) if '<Item ' in l]
                    last_model_idx = models[-1]
                    captured_lines = prev_lines[last_model_idx:] + [line]
                    open_items = sum(1 for l in captured_lines if '<Item ' in l) - sum(1 for l in captured_lines if '</Item>' in l)
                else:
                    prev_lines.append(line)
                    if len(prev_lines) > 50:
                        prev_lines.pop(0)
            else:
                captured_lines.append(line)
                if '<Item ' in line:
                    open_items += 1
                if '</Item>' in line:
                    open_items -= 1
                    if open_items <= 0:
                        break
                        
    xml_str = "".join(captured_lines)
    root = ET.fromstring(xml_str)
    
    parts = root.findall(".//Item[@class='Part']")
    print(f"Total parts: {len(parts)}")
    
    doors = []
    windows = []
    walls = []
    floors = []
    
    for p in parts:
        p_name = p.find("./Properties/string[@name='Name']").text
        cf = p.find("./Properties/CoordinateFrame[@name='CFrame']")
        sz = p.find("./Properties/Vector3[@name='size']")
        if cf is None or sz is None:
            continue
        x = float(cf.find("X").text)
        y = float(cf.find("Y").text)
        z = float(cf.find("Z").text)
        sx = float(sz.find("X").text)
        sy = float(sz.find("Y").text)
        sz_val = float(sz.find("Z").text)
        
        info = (p_name, x, y, z, sx, sy, sz_val)
        if "Puerta" in p_name or "door" in p_name.lower():
            doors.append(info)
        elif "window" in p_name.lower() or "fixtures_windows" in p_name.lower():
            windows.append(info)
        elif "wall" in p_name.lower():
            walls.append(info)
        elif "suelo" in p_name.lower() or "floor" in p_name.lower():
            floors.append(info)
            
    print(f"Doors ({len(doors)}):")
    for d in doors:
        print(f"  {d[0]} at ({d[1]:.2f}, {d[2]:.2f}, {d[3]:.2f}) size=({d[4]:.2f}, {d[5]:.2f}, {d[6]:.2f})")
        
    print(f"Windows ({len(windows)}):")
    for w in windows[:10]:
        print(f"  {w[0]} at ({w[1]:.2f}, {w[2]:.2f}, {w[3]:.2f}) size=({w[4]:.2f}, {w[5]:.2f}, {w[6]:.2f})")
        
    print(f"Walls ({len(walls)}):")
    min_x = min(w[1] - w[4]/2 for w in walls) if walls else 0
    max_x = max(w[1] + w[4]/2 for w in walls) if walls else 0
    min_z = min(w[3] - w[6]/2 for w in walls) if walls else 0
    max_z = max(w[3] + w[6]/2 for w in walls) if walls else 0
    min_y = min(w[2] - w[5]/2 for w in walls) if walls else 0
    max_y = max(w[2] + w[5]/2 for w in walls) if walls else 0
    print(f"  Wall bounds: X:[{min_x:.2f}..{max_x:.2f}] (span {max_x-min_x:.2f} studs, {(max_x-min_x)/3:.1f} tiles)")
    print(f"               Y:[{min_y:.2f}..{max_y:.2f}] (height {max_y-min_y:.2f} studs)")
    print(f"               Z:[{min_z:.2f}..{max_z:.2f}] (span {max_z-min_z:.2f} studs, {(max_z-min_z)/3:.1f} tiles)")

inspect_house_detailed("Livingroom_31_45_28")
inspect_house_detailed("Livingroom_31_45_33")
inspect_house_detailed("Derelict_31_45_22")

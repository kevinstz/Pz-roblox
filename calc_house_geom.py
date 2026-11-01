import xml.etree.ElementTree as ET

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def get_building_geometry(target_name):
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
    
    walls = []
    doors = []
    windows = []
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
        item = (p_name, x, y, z, sx, sy, sz_val)
        
        if "puerta" in p_name.lower():
            doors.append(item)
        elif "window" in p_name.lower() and "curtain" not in p_name.lower():
            windows.append(item)
        elif "wall" in p_name.lower():
            walls.append(item)
            
    print(f"\n================ {target_name} ================")
    # Exterior bounds
    min_x = min(w[1] - w[4]/2 for w in walls)
    max_x = max(w[1] + w[4]/2 for w in walls)
    min_z = min(w[3] - w[6]/2 for w in walls)
    max_z = max(w[3] + w[6]/2 for w in walls)
    print(f"Bounding Box: X=[{min_x:.2f} .. {max_x:.2f}] (width {max_x-min_x:.2f} studs)")
    print(f"              Z=[{min_z:.2f} .. {max_z:.2f}] (length {max_z-min_z:.2f} studs)")
    
    print(f"Doors ({len(doors)}):")
    for d in doors:
        print(f"  {d[0]} at ({d[1]:.2f}, {d[2]:.2f}, {d[3]:.2f}) sz=({d[4]:.2f}, {d[5]:.2f}, {d[6]:.2f})")
        
    print(f"Windows ({len(windows)}):")
    for w in windows:
        print(f"  {w[0]} at ({w[1]:.2f}, {w[2]:.2f}, {w[3]:.2f}) sz=({w[4]:.2f}, {w[5]:.2f}, {w[6]:.2f})")
    
    return min_x, max_x, min_z, max_z, doors, windows

get_building_geometry("Livingroom_31_45_28")
get_building_geometry("Livingroom_31_45_33")
get_building_geometry("Derelict_31_45_22")

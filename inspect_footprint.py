import xml.etree.ElementTree as ET

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def inspect_house_footprint(target_name):
    print(f"\n==========================================")
    print(f"FOOTPRINT INSPECTION: {target_name}")
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
    
    # Collect all exterior walls and doors
    ext_walls = []
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
        
        # Check if wall
        if "wall" in p_name.lower() or "puerta" in p_name.lower() or "door" in p_name.lower():
            ext_walls.append((p_name, x, y, z, sx, sy, sz_val))
            
    print(f"Found {len(ext_walls)} wall/door parts.")
    for w in ext_walls:
        print(f"  {w[0]:<35} pos=({w[1]:6.2f}, {w[2]:5.2f}, {w[3]:6.2f}) sz=({w[4]:5.2f}, {w[5]:5.2f}, {w[6]:5.2f})")

inspect_house_footprint("Livingroom_31_45_28")
inspect_house_footprint("Livingroom_31_45_33")

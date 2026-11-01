import xml.etree.ElementTree as ET
import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Let's inspect Suelo_Piso_1 parts near Livingroom_31_45_33 (X: 140..175, Z: 5..45)
# and near Livingroom_31_45_28 (X: 170..195, Z: -255..-215)

def scan_model_parts(model_name):
    print(f"Scanning {model_name}...")
    inside = False
    open_items = 0
    captured_lines = []
    
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        prev_lines = []
        for line in f:
            if not inside:
                if f'<string name="Name">{model_name}</string>' in line:
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
    print(f"Found {len(parts)} parts in {model_name}")
    
    # Check parts near House 33 and House 28
    near_33 = []
    near_28 = []
    for p in parts:
        cf = p.find("./Properties/CoordinateFrame[@name='CFrame']")
        sz = p.find("./Properties/Vector3[@name='size']")
        p_name = p.find("./Properties/string[@name='Name']")
        p_nm = p_name.text if p_name is not None else ""
        if cf is not None and sz is not None:
            x = float(cf.find("X").text)
            y = float(cf.find("Y").text)
            z = float(cf.find("Z").text)
            sx = float(sz.find("X").text)
            sy = float(sz.find("Y").text)
            sz_val = float(sz.find("Z").text)
            
            if 140 <= x <= 175 and 5 <= z <= 45:
                near_33.append((p_nm, x, y, z, sx, sy, sz_val))
            elif 170 <= x <= 195 and -255 <= z <= -215:
                near_28.append((p_nm, x, y, z, sx, sy, sz_val))
                
    print(f"Near House 33 (X: 140..175, Z: 5..45): {len(near_33)} parts")
    for item in near_33:
        print(f"  {item[0]} pos=({item[1]:.1f}, {item[2]:.1f}, {item[3]:.1f}) sz=({item[4]:.1f}, {item[5]:.1f}, {item[6]:.1f})")
        
    print(f"Near House 28 (X: 170..195, Z: -255..-215): {len(near_28)} parts")
    for item in near_28:
        print(f"  {item[0]} pos=({item[1]:.1f}, {item[2]:.1f}, {item[3]:.1f}) sz=({item[4]:.1f}, {item[5]:.1f}, {item[6]:.1f})")

scan_model_parts("Suelo_Piso_1")

import xml.etree.ElementTree as ET

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def inspect_with_depth_counter(target_name):
    inside = False
    open_items = 0
    captured_lines = []
    
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        prev_lines = []
        for line in f:
            if not inside:
                if f'<string name="Name">{target_name}</string>' in line:
                    inside = True
                    # Find the <Item class="Model" line from prev_lines
                    models = [i for i, l in enumerate(prev_lines) if '<Item class="Model"' in l]
                    last_model_idx = models[-1]
                    captured_lines = prev_lines[last_model_idx:] + [line]
                    # Count open items in captured lines
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
    
    # Analyze root
    parts = root.findall(".//Item[@class='Part']")
    print(f"=== {target_name} ===")
    print(f"Total parts: {len(parts)}")
    
    xs, ys, zs = [], [], []
    texs = set()
    names = set()
    for p in parts:
        p_name = p.find("./Properties/string[@name='Name']")
        p_name_val = p_name.text if p_name is not None else ""
        names.add(p_name_val)
        
        # CFrame or position
        cf = p.find("./Properties/CoordinateFrame[@name='CFrame']")
        if cf is not None:
            x = float(cf.find("X").text)
            y = float(cf.find("Y").text)
            z = float(cf.find("Z").text)
            xs.append(x)
            ys.append(y)
            zs.append(z)
            
        for d in p.findall(".//Item[@class='Decal']"):
            t = d.find("./Properties/string[@name='Texture']")
            if t is not None and t.text:
                texs.add(t.text.split('/')[-1])
        for t in p.findall(".//Item[@class='Texture']"):
            tx = t.find("./Properties/string[@name='Texture']")
            if tx is not None and tx.text:
                texs.add(tx.text.split('/')[-1])
                
    if xs:
        print(f"  X: {min(xs):.1f} to {max(xs):.1f} (span {max(xs)-min(xs):.1f} studs, {(max(xs)-min(xs))/3.0:.1f} tiles)")
        print(f"  Y: {min(ys):.1f} to {max(ys):.1f} (span {max(ys)-min(ys):.1f} studs)")
        print(f"  Z: {min(zs):.1f} to {max(zs):.1f} (span {max(zs)-min(zs):.1f} studs, {(max(zs)-min(zs))/3.0:.1f} tiles)")
    print(f"  Sample names ({len(names)}): {list(names)[:10]}")
    print(f"  Sample textures ({len(texs)}): {list(texs)[:10]}")

inspect_with_depth_counter("Livingroom_31_45_28")
inspect_with_depth_counter("Livingroom_31_45_33")

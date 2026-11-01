import xml.etree.ElementTree as ET

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Let's inspect all 14 buildings
buildings_list = [
    "Banco_31_45_3",
    "Derelict_31_45_5",
    "Chinesekitchen_31_45_4",
    "Cafe_31_45_7",
    "Office_31_45_9",
    "Libreria_31_45_23",
    "Livingroom_31_45_28",
    "Office_31_45_8",
    "Derelict_31_45_22",
    "Bar_31_45_12",
    "Office_31_45_24",
    "Livingroom_31_45_33",
    "Comisaria_31_45_38",
    "EstacionBomberos_31_45_42"
]

def inspect_all():
    inside_name = None
    open_items = 0
    captured_lines = []
    
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        prev_lines = []
        for line in f:
            if inside_name is None:
                for b_name in buildings_list:
                    if f'<string name="Name">{b_name}</string>' in line:
                        inside_name = b_name
                        models = [i for i, l in enumerate(prev_lines) if '<Item ' in l]
                        last_model_idx = models[-1]
                        captured_lines = prev_lines[last_model_idx:] + [line]
                        open_items = sum(1 for l in captured_lines if '<Item ' in l) - sum(1 for l in captured_lines if '</Item>' in l)
                        break
                if inside_name is None:
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
                        xml_str = "".join(captured_lines)
                        root = ET.fromstring(xml_str)
                        parts = root.findall(".//Item[@class='Part']")
                        xs = [float(p.find("./Properties/CoordinateFrame[@name='CFrame']/X").text) for p in parts if p.find("./Properties/CoordinateFrame[@name='CFrame']") is not None]
                        zs = [float(p.find("./Properties/CoordinateFrame[@name='CFrame']/Z").text) for p in parts if p.find("./Properties/CoordinateFrame[@name='CFrame']") is not None]
                        floors = [m.find("./Properties/string[@name='Name']").text for m in root.findall(".//Item[@class='Model']") if m.find("./Properties/string[@name='Name']") is not None and m.find("./Properties/string[@name='Name']").text.startswith("Piso_")]
                        
                        dx = max(xs) - min(xs) if xs else 0
                        dz = max(zs) - min(zs) if zs else 0
                        print(f"{inside_name:<26} | parts: {len(parts):<4} | floors: {','.join(floors):<18} | X:[{min(xs):.1f}..{max(xs):.1f}]({dx:.1f}s/{dx/3:.1f}t) | Z:[{min(zs):.1f}..{max(zs):.1f}]({dz:.1f}s/{dz/3:.1f}t)")
                        
                        inside_name = None
                        captured_lines = []

inspect_all()

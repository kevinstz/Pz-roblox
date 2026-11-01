rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Find building model names inside Edificios that have parts at:
# 1. Left building: X in [-70, -20], Z in [-80, -20]
# 2. Right building: X in [0, 50], Z in [-80, -20]

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_edif = False
    current_building = ""
    left_counts = {}
    right_counts = {}
    
    current_part = {}
    
    for line in f:
        if 'name="Name">Edificios<' in line:
            in_edif = True
            continue
        if in_edif:
            if 'name="Name">Exterior<' in line:
                break
            if '<Item class="Model"' in line:
                pass
            if '<string name="Name">' in line:
                val = line.split('>')[1].split('<')[0]
                if any(val.startswith(p) for p in ["Banco", "Derelict", "Chinese", "Cafe", "Office", "Libreria", "Livingroom", "Bar", "Comisaria", "Estacion"]):
                    current_building = val
            if '<Item class="Part"' in line or '<Item class="WedgePart"' in line or '<Item class="CornerWedgePart"' in line:
                current_part = {'x': None, 'y': None, 'z': None, 'name': ''}
            if current_part:
                if '<string name="Name">' in line and not current_part['name']:
                    current_part['name'] = line.split('>')[1].split('<')[0]
                if '<X>' in line and '</X>' in line and current_part['x'] is None:
                    try: current_part['x'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '<Y>' in line and '</Y>' in line and current_part['y'] is None:
                    try: current_part['y'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '<Z>' in line and '</Z>' in line and current_part['z'] is None:
                    try: current_part['z'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '</Item>' in line and current_part['x'] is not None and current_part['z'] is not None:
                    x, z = current_part['x'], current_part['z']
                    if -70 <= x <= -20 and -80 <= z <= -20:
                        left_counts[current_building] = left_counts.get(current_building, 0) + 1
                    elif 0 <= x <= 50 and -80 <= z <= -20:
                        right_counts[current_building] = right_counts.get(current_building, 0) + 1
                    current_part = {}

print("Left building candidates (X: -70..-20, Z: -80..-20):", left_counts)
print("Right building candidates (X: 0..50, Z: -80..-20):", right_counts)

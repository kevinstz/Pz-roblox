rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_bar = False
    current_part = {}
    roof_parts = []
    
    for line in f:
        if 'name="Name">Bar_31_45_12<' in line:
            in_bar = True
            continue
        if in_bar:
            if 'referent="R93579"' in line:
                break
            if '<Item class="' in line and ('Part' in line or 'Wedge' in line or 'Mesh' in line):
                cls = line.split('"')[1]
                current_part = {'class': cls, 'name': '', 'x': None, 'y': None, 'z': None, 'sx': None, 'sy': None, 'sz': None}
                continue
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
                if '</Item>' in line and current_part.get('class'):
                    pname = current_part['name'].lower()
                    if 'roof' in pname or 'wedge' in current_part['class'].lower() or 'cornice' in pname or 'wall' in pname:
                        x, y, z = current_part['x'], current_part['y'], current_part['z']
                        if x is not None and z is not None:
                            if -60 <= x <= -10 and -70 <= z <= -20:
                                roof_parts.append((current_part['name'], current_part['class'], x, y, z))
                    current_part = {}

print(f"Total roof/wall parts in Bar region: {len(roof_parts)}")
for p in roof_parts:
    print(p)

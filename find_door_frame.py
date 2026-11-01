rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

# Look for parts in Bar_31_45_12
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_bar = False
    current_part = {}
    
    for line in f:
        if 'name="Name">Bar_31_45_12<' in line:
            in_bar = True
            continue
        if in_bar:
            if 'referent="R93579"' in line:
                break
            if '<Item class="' in line:
                cls = line.split('"')[1]
                current_part = {'class': cls, 'lines': [line], 'name': '', 'x': None, 'y': None, 'z': None, 'sx': None, 'sy': None, 'sz': None}
                continue
            if current_part:
                current_part['lines'].append(line)
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
                if '</Item>' in line:
                    x, y, z = current_part['x'], current_part['y'], current_part['z']
                    if x is not None and z is not None:
                        # Check if near the front corner: X: -45..-25, Z: -55..-30
                        if -45 <= x <= -25 and -55 <= z <= -30:
                            pname = current_part['name']
                            # Check if it has a mesh or special shape
                            full_text = "".join(current_part['lines'])
                            if 'SpecialMesh' in full_text or 'Mesh' in full_text or 'arch' in pname.lower() or 'door' in pname.lower() or 'frame' in pname.lower() or 'trim' in pname.lower() or 'white' in pname.lower():
                                print(f"Part: {pname} ({current_part['class']}) at ({x}, {y}, {z})")
                    current_part = {}

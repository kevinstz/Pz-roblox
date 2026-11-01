rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    hierarchy = []
    current_part = {}
    
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)"', line)
        if m_item:
            hierarchy.append(m_item.group(1))
            current_part = {'class': m_item.group(1), 'name': '', 'x': None, 'y': None, 'z': None}
            continue
        if '</Item>' in line:
            if current_part and current_part.get('x') is not None and current_part.get('z') is not None:
                x, y, z = current_part['x'], current_part['y'], current_part['z']
                if -60 <= x <= 0 and -80 <= z <= -20:
                    bld = "Unknown"
                    for h in reversed(hierarchy):
                        if any(h.startswith(prefix) for prefix in ["Banco", "Derelict", "Chinese", "Cafe", "Office", "Libreria", "Livingroom", "Bar", "Comisaria", "Estacion"]):
                            bld = h
                            break
                    if bld == "Unknown":
                        print(f"Unknown part at ({x:.1f}, {y:.1f}, {z:.1f}): name='{current_part['name']}', hierarchy={hierarchy[-4:]}")
            if hierarchy:
                hierarchy.pop()
            current_part = {}
            continue
            
        if '<string name="Name">' in line:
            name = line.split('>')[1].split('<')[0]
            if hierarchy:
                hierarchy[-1] = name
            if current_part:
                current_part['name'] = name
        if current_part:
            if '<X>' in line and '</X>' in line and current_part['x'] is None:
                try: current_part['x'] = float(line.split('>')[1].split('<')[0])
                except: pass
            elif '<Y>' in line and '</Y>' in line and current_part['y'] is None:
                try: current_part['y'] = float(line.split('>')[1].split('<')[0])
                except: pass
            elif '<Z>' in line and '</Z>' in line and current_part['z'] is None:
                try: current_part['z'] = float(line.split('>')[1].split('<')[0])
                except: pass

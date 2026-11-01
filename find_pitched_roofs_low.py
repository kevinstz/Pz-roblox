rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Find all parts with roof or wedge at Y between 5.0 and 12.0
import re

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_edif = False
    cur_bld = ""
    cur_p = {}
    found = []
    
    for line in f:
        if 'name="Name">Edificios<' in line:
            in_edif = True
            continue
        if in_edif:
            if 'name="Name">Exterior<' in line:
                break
            if '<string name="Name">' in line:
                val = line.split('>')[1].split('<')[0]
                if any(val.startswith(pfx) for pfx in ["Banco_", "Derelict_", "Chinesekitchen_", "Cafe_", "Office_", "Libreria_", "Livingroom_", "Bar_", "Comisaria_", "EstacionBomberos_"]):
                    cur_bld = val
            if '<Item class="' in line and ('Part' in line or 'Wedge' in line or 'Mesh' in line):
                cls = line.split('"')[1]
                cur_p = {'class': cls, 'lines': [line], 'name': '', 'x': None, 'y': None, 'z': None}
                continue
            if cur_p:
                cur_p['lines'].append(line)
                if '<string name="Name">' in line and not cur_p['name']:
                    cur_p['name'] = line.split('>')[1].split('<')[0]
                if '<CoordinateFrame name="CFrame">' in line:
                    pass
                if '<X>' in line and cur_p['x'] is None:
                    try: cur_p['x'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '<Y>' in line and cur_p['y'] is None:
                    try: cur_p['y'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '<Z>' in line and cur_p['z'] is None:
                    try: cur_p['z'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '</Item>' in line and cur_p.get('class'):
                    x, y, z = cur_p['x'], cur_p['y'], cur_p['z']
                    if y is not None and 5.0 <= y <= 13.0:
                        pname = cur_p['name'].lower()
                        if 'roof' in pname or 'wedge' in cur_p['class'].lower() or 'cornice' in pname:
                            found.append((cur_bld, cur_p['name'], cur_p['class'], x, y, z))
                    cur_p = {}

print(f"Total pitched roof parts at Y=5..13: {len(found)}")
for p in found:
    print(p)

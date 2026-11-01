import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def parse_items():
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        in_edif = False
        stack = []
        parts = []
        
        for line in f:
            if 'name="Name">Edificios<' in line:
                in_edif = True
                continue
            if in_edif:
                if 'name="Name">Exterior<' in line:
                    break
                m_open = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
                if m_open:
                    item = {'class': m_open.group(1), 'ref': m_open.group(2), 'name': '', 'x': None, 'y': None, 'z': None, 'in_cframe': False, 'size': None, 'children': []}
                    stack.append(item)
                    continue
                if '</Item>' in line:
                    if stack:
                        item = stack.pop()
                        if item['class'] in ('Part', 'WedgePart', 'CornerWedgePart', 'MeshPart') and item['x'] is not None:
                            # parent building name
                            bld = "Unknown"
                            for p in stack:
                                if any(p['name'].startswith(pfx) for pfx in ["Banco_", "Derelict_", "Chinesekitchen_", "Cafe_", "Office_", "Libreria_", "Livingroom_", "Bar_", "Comisaria_", "EstacionBomberos_"]):
                                    bld = p['name']
                                    break
                            parts.append((bld, item['name'], item['class'], item['x'], item['y'], item['z'], item['ref']))
                    continue
                if stack:
                    curr = stack[-1]
                    if '<string name="Name">' in line and not curr['name']:
                        curr['name'] = line.split('>')[1].split('<')[0]
                    elif '<CoordinateFrame name="CFrame">' in line:
                        curr['in_cframe'] = True
                    elif curr.get('in_cframe'):
                        if '<X>' in line and curr['x'] is None:
                            try: curr['x'] = float(line.split('>')[1].split('<')[0])
                            except: pass
                        elif '<Y>' in line and curr['y'] is None:
                            try: curr['y'] = float(line.split('>')[1].split('<')[0])
                            except: pass
                        elif '<Z>' in line and curr['z'] is None:
                            try: curr['z'] = float(line.split('>')[1].split('<')[0])
                            except: pass
                        elif '</CoordinateFrame>' in line:
                            curr['in_cframe'] = False

    print(f"Total parts parsed in Edificios: {len(parts)}")
    return parts

parts = parse_items()
# Filter to region near the cars: X in [30, 120], Z in [-100, 0]
region_parts = [p for p in parts if 30 <= p[3] <= 120 and -100 <= p[5] <= 0]
print(f"Parts in car region (X: 30..120, Z: -100..0): {len(region_parts)}")

# Count by building
blds = {}
for p in region_parts:
    blds[p[0]] = blds.get(p[0], 0) + 1
print("Buildings in region:", blds)

# Sample parts by name prefix
types = {}
for p in region_parts:
    t = p[1].split('_')[0]
    types[t] = types.get(t, 0) + 1
print("Part types in region:", types)

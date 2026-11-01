rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

# Search for the trash can next to the car:
# Look for cylinder/trashcan near each pair of cars!
car_pairs = [
    ("Pair 1", -78.0, -138.0),
    ("Pair 2", -21.0, -60.0),
    ("Pair 3", 69.0, -66.0),
    ("Pair 4", 153.0, -150.0),
]

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    stack = []
    found = []
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
        if m_item:
            stack.append({'class': m_item.group(1), 'ref': m_item.group(2), 'name': '', 'x': None, 'y': None, 'z': None, 'in_cf': False})
            continue
        if '</Item>' in line:
            if stack:
                it = stack.pop()
                if it['x'] is not None and it['name']:
                    x, y, z = it['x'], it['y'], it['z']
                    for name, cx, cz in car_pairs:
                        if abs(x - cx) < 40 and abs(z - cz) < 40:
                            if any(k in it['name'].lower() for k in ['trash', 'bench', 'canopy', 'awning', 'hedge', 'porch']):
                                found.append((name, it['name'], it['class'], x, y, z, [s['name'] for s in stack[-2:]]))
            continue
        if stack:
            cur = stack[-1]
            if '<string name="Name">' in line and not cur['name']:
                cur['name'] = line.split('>')[1].split('<')[0]
            elif '<CoordinateFrame name="CFrame">' in line:
                cur['in_cf'] = True
            elif cur.get('in_cf'):
                if '<X>' in line and cur['x'] is None:
                    try: cur['x'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '<Y>' in line and cur['y'] is None:
                    try: cur['y'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                if '<Z>' in line and cur['z'] is None:
                    try: cur['z'] = float(line.split('>')[1].split('<')[0])
                    except: pass
                elif '</CoordinateFrame>' in line:
                    cur['in_cf'] = False

print(f"Total matching props near car pairs: {len(found)}")
for p in found:
    print(f"Near {p[0]}: {p[1]} ({p[2]}) at ({p[3]:.1f}, {p[4]:.1f}, {p[5]:.1f}) in {p[6]}")

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

# Search for the hedge and dumpster corral
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
                if it['name'] and any(k in it['name'].lower() for k in ['hedge', 'trashcontainers', 'dumpster', 'fence_wood', 'vegetation_outdoor']):
                    if it['x'] is not None:
                        found.append((it['name'], it['class'], it['x'], it['y'], it['z'], [s['name'] for s in stack[-2:]]))
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

print(f"Total matching props found: {len(found)}")
for p in found:
    # Filter to X near 0..120, Z near -100..0
    if 20 <= p[2] <= 120 and -100 <= p[4] <= 0:
        print(f"{p[0]} ({p[1]}) at ({p[2]:.1f}, {p[3]:.1f}, {p[4]:.1f}) in {p[5]}")

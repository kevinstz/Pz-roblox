rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

# Let's search for:
# 1. Any part with "arch" or SpecialMesh with mesh type or MeshPart in all of Edificios and Exterior
# 2. Any part near the windows of Libreria (X around 40..120, Z around -100..-70, Y around 7..15)
#    that is rotated or sticking out
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    stack = []
    special_parts = []
    rotated_in_lib = []
    
    for line in f:
        m_item = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
        if m_item:
            stack.append({'class': m_item.group(1), 'ref': m_item.group(2), 'name': '', 'x': None, 'y': None, 'z': None, 'in_cf': False, 'lines': [line]})
            continue
        if '</Item>' in line:
            if stack:
                it = stack.pop()
                if it['class'] in ('Part', 'WedgePart', 'CornerWedgePart', 'MeshPart') and it['x'] is not None:
                    text = "".join(it['lines'])
                    name = it['name']
                    x, y, z = it['x'], it['y'], it['z']
                    parents = [s['name'] for s in stack[-3:]]
                    
                    # 1. Check for mesh or arch
                    if 'Mesh' in text or 'arch' in name.lower() or 'door' in name.lower() and 'frame' in name.lower():
                        special_parts.append((name, it['class'], (x, y, z), parents, text[:300]))
                        
                    # 2. Check for rotated parts in Libreria / nearby Exterior
                    m_rot = re.findall(r'<R\d\d>([^<]+)</R\d\d>', text)
                    is_rot = any(abs(float(r)) not in (0.0, 1.0) for r in m_rot) if m_rot else False
                    if is_rot and 30 <= x <= 125 and -110 <= z <= -60:
                        rotated_in_lib.append((name, it['class'], (x, y, z), parents, it['ref']))
                continue
        if stack:
            cur = stack[-1]
            cur['lines'].append(line)
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

print(f"Total special/arch/mesh parts: {len(special_parts)}")
for p in special_parts[:15]:
    print(p[0], p[1], p[2], p[3])

print(f"\nTotal rotated parts in Libreria region: {len(rotated_in_lib)}")
for p in rotated_in_lib:
    print(p[0], p[1], f"pos=({p[2][0]:.2f}, {p[2][1]:.2f}, {p[2][2]:.2f})", p[3], p[4])

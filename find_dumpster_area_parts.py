import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def get_props_near_dumpster():
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        stack = []
        found = []
        for line in f:
            m_item = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
            if m_item:
                stack.append({'class': m_item.group(1), 'ref': m_item.group(2), 'name': '', 'x': None, 'y': None, 'z': None, 'in_cf': False, 'lines': [line]})
                continue
            if '</Item>' in line:
                if stack:
                    it = stack.pop()
                    if it['class'] in ('Part', 'WedgePart', 'CornerWedgePart', 'MeshPart') and it['x'] is not None:
                        x, y, z = it['x'], it['y'], it['z']
                        if 105 <= x <= 125 and -100 <= z <= -70:
                            parents = [s['name'] for s in stack[-3:]]
                            found.append((it['name'], it['class'], x, y, z, parents, "".join(it['lines'])))
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
                    elif '<Y>' in line and cur['y'] is None:
                        try: cur['y'] = float(line.split('>')[1].split('<')[0])
                        except: pass
                    elif '<Z>' in line and cur['z'] is None:
                        try: cur['z'] = float(line.split('>')[1].split('<')[0])
                        except: pass
                    elif '</CoordinateFrame>' in line:
                        cur['in_cf'] = False
        return found

found = get_props_near_dumpster()
print(f"Total parts found near dumpster and windows: {len(found)}")
for p in found:
    text = p[6]
    m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
    sz = m_sz.groups() if m_sz else ("?", "?", "?")
    m_rot = re.findall(r'<R\d\d>([^<]+)</R\d\d>', text)
    is_rotated = any(abs(float(r)) not in (0.0, 1.0) for r in m_rot) if m_rot else False
    if is_rotated or p[3] > 6.0 or 'window' in p[0].lower() or 'fence' in p[0].lower() or 'roof' in p[0].lower() or 'wedge' in p[1].lower():
        print(f"Name={p[0]}, Class={p[1]}, pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}), sz={sz}, rotated={is_rotated}, parents={p[5]}")

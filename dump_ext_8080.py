import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def dump_exterior_8080():
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        in_ext = False
        stack = []
        parts = []
        for line in f:
            if 'name="Name">Exterior_8080_11648<' in line:
                in_ext = True
                continue
            if in_ext:
                if '</Item>' in line and len(stack) == 1:
                    break
                m_item = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
                if m_item:
                    stack.append({'class': m_item.group(1), 'ref': m_item.group(2), 'name': '', 'x': None, 'y': None, 'z': None, 'in_cf': False, 'lines': [line]})
                    continue
                if '</Item>' in line:
                    if stack:
                        it = stack.pop()
                        if it['class'] in ('Part', 'WedgePart', 'CornerWedgePart', 'MeshPart') and it['x'] is not None:
                            parts.append((it['name'], it['class'], it['x'], it['y'], it['z'], it['ref'], "".join(it['lines'])))
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
        return parts

parts = dump_exterior_8080()
print(f"Total parts in Exterior_8080_11648: {len(parts)}")
types = {}
for p in parts:
    t = p[0].split('_')[0]
    types[t] = types.get(t, 0) + 1
print("Part types:", types)

# Print walls, roofs, wedges, etc.
for p in parts:
    pname = p[0].lower()
    if any(k in pname for k in ['wall', 'roof', 'window', 'door', 'wedge', 'cornice', 'trim', 'deck']):
        print(f"Ref={p[5]}, Name={p[0]}, Class={p[1]}, pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f})")

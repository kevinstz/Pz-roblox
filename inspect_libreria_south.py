import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def get_libreria_south_parts():
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        in_libreria = False
        stack = []
        parts = []
        
        for line in f:
            if 'name="Name">Libreria_31_45_23<' in line:
                in_libreria = True
                continue
            if in_libreria:
                if 'name="Name">Livingroom_31_45_28<' in line:
                    break
                m_open = re.search(r'<Item class="([^"]+)" referent="([^"]+)"', line)
                if m_open:
                    item = {'class': m_open.group(1), 'ref': m_open.group(2), 'name': '', 'x': None, 'y': None, 'z': None, 'in_cframe': False, 'lines': [line]}
                    stack.append(item)
                    continue
                if '</Item>' in line:
                    if stack:
                        item = stack.pop()
                        if item['class'] in ('Part', 'WedgePart', 'CornerWedgePart', 'MeshPart') and item['x'] is not None:
                            z = item['z']
                            # South side of Libreria facing parking lot: Z in [-95, -70]
                            if -95 <= z <= -70:
                                parts.append(item)
                    continue
                if stack:
                    curr = stack[-1]
                    curr['lines'].append(line)
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

    return parts

parts = get_libreria_south_parts()
print(f"Total parts on south of Libreria (facing parking lot): {len(parts)}")
for p in parts:
    text = "".join(p['lines'])
    m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
    sz = m_sz.groups() if m_sz else ("?", "?", "?")
    m_mat = re.search(r'<token name="Material">([^<]+)</token>', text)
    mat = m_mat.group(1) if m_mat else "?"
    decals = re.findall(r'<string name="Texture">([^<]+)</string>', text)
    print(f"Ref={p['ref']}, Name={p['name']}, Class={p['class']}, pos=({p['x']:.2f}, {p['y']:.2f}, {p['z']:.2f}), sz={sz}, mat={mat}, tex={decals[:2]}")

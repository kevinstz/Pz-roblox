import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

# Find all parts in Bar_31_45_12 with X >= -54
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_bar = False
    cur_p = {}
    found = []
    
    for line in f:
        if 'name="Name">Bar_31_45_12<' in line:
            in_bar = True
            continue
        if in_bar:
            if 'referent="R93579"' in line:
                break
            if '<Item class="' in line and ('Part' in line or 'Wedge' in line or 'Mesh' in line):
                cls = line.split('"')[1]
                cur_p = {'class': cls, 'lines': [line], 'name': '', 'x': None, 'y': None, 'z': None, 'size': []}
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
                    if x is not None and x >= -54.0:
                        text = "".join(cur_p['lines'])
                        m_size = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                        size_str = m_size.groups() if m_size else ("?", "?", "?")
                        m_mat = re.search(r'<token name="Material">([^<]+)</token>', text)
                        mat = m_mat.group(1) if m_mat else "?"
                        decals = re.findall(r'<string name="Texture">([^<]+)</string>', text)
                        found.append((cur_p['name'], cur_p['class'], (x, y, z), size_str, mat, decals))
                    cur_p = {}

print(f"Total parts on east facade of Bar_31_45_12: {len(found)}")
for p in found:
    print(p[0], p[1], f"pos=({p[2][0]:.1f}, {p[2][1]:.1f}, {p[2][2]:.1f})", f"sz={p[3]}", f"mat={p[4]}", f"tex={p[5]}")

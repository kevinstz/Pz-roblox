rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

# Search for parts whose size is roughly a doorway or window surround:
# Height ~ 6 to 10 studs, width ~ 3 to 6 studs, depth < 1.5 studs
# And has color white (e.g. 255, 255, 255 or 163 / 240+ or SmoothPlastic or Mesh)
def find_arch_door():
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
                    if it['class'] in ('Part', 'WedgePart', 'MeshPart') and it['x'] is not None:
                        text = "".join(it['lines'])
                        # Check size
                        m_sz = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', text)
                        if m_sz:
                            sx, sy, sz = float(m_sz.group(1)), float(m_sz.group(2)), float(m_sz.group(3))
                            # Door/frame size: sy between 5 and 12, (sx between 2.5 and 7 or sz between 2.5 and 7)
                            if 5.0 <= sy <= 12.0 and (2.5 <= sx <= 7.0 or 2.5 <= sz <= 7.0):
                                x, y, z = it['x'], it['y'], it['z']
                                # In our downtown Rosewood area:
                                if -100 <= x <= 150 and -200 <= z <= 50:
                                    # Check if white or SpecialMesh or no texture
                                    decals = re.findall(r'<string name="Texture">([^<]+)</string>', text)
                                    m_col = re.search(r'<Color3uint8 name="Color3uint8">(\d+)</Color3uint8>', text)
                                    col = int(m_col.group(1)) if m_col else 0
                                    parents = [s['name'] for s in stack[-2:]]
                                    found.append((it['name'], it['class'], it['ref'], (x, y, z), (sx, sy, sz), col, len(decals), parents))
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

found = find_arch_door()
print(f"Total doorway/frame-sized parts: {len(found)}")
# Filter to parts with 0 decals (untextured!)
untextured = [p for p in found if p[6] == 0]
print(f"Untextured: {len(untextured)}")
for p in untextured[:30]:
    print(f"Ref={p[2]}, Name={p[0]}, Class={p[1]}, pos=({p[3][0]:.1f}, {p[3][1]:.1f}, {p[3][2]:.1f}), sz={p[4]}, col={p[5]}, parents={p[7]}")

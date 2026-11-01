import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

def dump_pair2_region():
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
                        # Bounding box around Pair 2 scene:
                        if -100 <= x <= 10 and -100 <= z <= 0:
                            parents = [s['name'] for s in stack[-2:]]
                            found.append((it['name'], it['class'], x, y, z, parents, "".join(it['lines']), it['ref']))
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

found = dump_pair2_region()
print(f"Total parts in Pair 2 region: {len(found)}")

# Group by parent
by_parent = {}
for p in found:
    parent_str = " -> ".join(p[5])
    by_parent[parent_str] = by_parent.get(parent_str, 0) + 1
for k, v in sorted(by_parent.items()):
    print(f"  {k}: {v} parts")

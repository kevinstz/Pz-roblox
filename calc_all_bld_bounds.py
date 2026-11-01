rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

buildings = {}

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_edif = False
    cur_bld = ""
    in_cframe = False
    cur_x, cur_y, cur_z = None, None, None
    for line in f:
        if 'name="Name">Edificios<' in line:
            in_edif = True
            continue
        if in_edif:
            if 'name="Name">Exterior<' in line:
                break
            if '<string name="Name">' in line:
                val = line.split('>')[1].split('<')[0]
                if any(val.startswith(pfx) for pfx in ["Banco_", "Derelict_", "Chinesekitchen_", "Cafe_", "Office_", "Libreria_", "Livingroom_", "Bar_", "Comisaria_", "EstacionBomberos_"]):
                    cur_bld = val
                    if cur_bld not in buildings:
                        buildings[cur_bld] = {'xs': [], 'ys': [], 'zs': []}
            if cur_bld:
                if '<CoordinateFrame name="CFrame">' in line:
                    in_cframe = True
                    cur_x, cur_y, cur_z = None, None, None
                elif in_cframe:
                    if '<X>' in line and cur_x is None:
                        try: cur_x = float(line.split('>')[1].split('<')[0])
                        except: pass
                    elif '<Y>' in line and cur_y is None:
                        try: cur_y = float(line.split('>')[1].split('<')[0])
                        except: pass
                    elif '<Z>' in line and cur_z is None:
                        try: cur_z = float(line.split('>')[1].split('<')[0])
                        except: pass
                    elif '</CoordinateFrame>' in line:
                        in_cframe = False
                        if cur_x is not None and cur_z is not None:
                            buildings[cur_bld]['xs'].append(cur_x)
                            buildings[cur_bld]['ys'].append(cur_y)
                            buildings[cur_bld]['zs'].append(cur_z)
                        cur_x, cur_y, cur_z = None, None, None

for name, data in sorted(buildings.items()):
    xs, ys, zs = data['xs'], data['ys'], data['zs']
    if xs:
        print(f"{name}: parts={len(xs)}, X=[{min(xs):.1f}, {max(xs):.1f}], Y=[{min(ys):.1f}, {max(ys):.1f}], Z=[{min(zs):.1f}, {max(zs):.1f}]")

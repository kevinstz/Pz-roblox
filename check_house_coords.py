rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for target in ["Livingroom_31_45_28", "Livingroom_31_45_33", "Derelict_31_45_22"]:
        f.seek(0)
        xs, ys, zs = [], [], []
        in_target = False
        for line in f:
            if f'name="Name">{target}<' in line:
                in_target = True
                continue
            if in_target:
                if '<Item class="Model"' in line and 'referent=' in line and len(xs) > 100:
                    # check if next building
                    pass
                if '<X>' in line and '</X>' in line:
                    try: xs.append(float(line.split('>')[1].split('<')[0]))
                    except: pass
                if '<Y>' in line and '</Y>' in line:
                    try: ys.append(float(line.split('>')[1].split('<')[0]))
                    except: pass
                if '<Z>' in line and '</Z>' in line:
                    try: zs.append(float(line.split('>')[1].split('<')[0]))
                    except: pass
                if len(xs) >= 200:
                    break
        if xs and zs:
            print(f"{target}: X=[{min(xs):.1f}, {max(xs):.1f}], Z=[{min(zs):.1f}, {max(zs):.1f}]")

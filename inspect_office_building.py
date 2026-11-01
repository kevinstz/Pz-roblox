rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_target = False
    target_name = "Office_31_45_24"
    floors = {}
    current_floor = ""
    part_types = {}
    
    for line in f:
        if f'name="Name">{target_name}<' in line:
            in_target = True
            print(f"Found {target_name}")
            continue
        if in_target:
            if '<string name="Name">Piso_' in line:
                current_floor = line.split('>')[1].split('<')[0]
                if current_floor not in floors:
                    floors[current_floor] = []
            if '<string name="Name">' in line and not line.strip().startswith('<string name="Name">Piso_'):
                pname = line.split('>')[1].split('<')[0]
                if current_floor:
                    floors[current_floor].append(pname)
            # check if end of Office_31_45_24
            if '<Item class="Model"' in line and 'referent="R102211"' in line: # next model is Livingroom_31_45_33
                print(f"End of {target_name}")
                break

for fl, pnames in floors.items():
    print(f"Floor {fl}: {len(pnames)} items. Sample names:")
    prefixes = {}
    for p in pnames:
        pfx = p.split('_')[0]
        prefixes[pfx] = prefixes.get(pfx, 0) + 1
    print(" ", prefixes)

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_veh = False
    vname = None
    coords = {}
    for line in f:
        if 'name="Name">Vehiculo_' in line:
            vname = line.split('>')[1].split('<')[0]
            in_veh = True
        elif in_veh:
            if '<X>' in line and 'X' not in coords:
                coords['X'] = line.split('>')[1].split('<')[0]
            elif '<Y>' in line and 'Y' not in coords:
                coords['Y'] = line.split('>')[1].split('<')[0]
            elif '<Z>' in line and 'Z' not in coords:
                coords['Z'] = line.split('>')[1].split('<')[0]
            if len(coords) == 3:
                print(f"{vname}: ({float(coords['X']):.1f}, {float(coords['Y']):.1f}, {float(coords['Z']):.1f})")
                in_veh = False
                coords = {}

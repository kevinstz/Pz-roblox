rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_veh = False
    in_cframe = False
    veh_name = ""
    for line in f:
        if 'name="Name">Vehiculos<' in line:
            in_veh = True
            print("Found Vehiculos folder")
            continue
        if in_veh:
            if '<Item class="Model"' in line:
                pass
            if '<string name="Name">' in line and not veh_name:
                veh_name = line.strip()
            if '<CoordinateFrame name="CFrame">' in line:
                in_cframe = True
            elif in_cframe and '<X>' in line:
                print(f"Vehicle: {veh_name}, pos: {line.strip()}", end=" ")
            elif in_cframe and '<Z>' in line:
                print(f"{line.strip()}")
                in_cframe = False
                veh_name = ""
            if '</Item>' in line and 'Vehiculos' in line:
                break

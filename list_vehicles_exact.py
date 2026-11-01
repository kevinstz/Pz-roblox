rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_veh = False
    cur_m = ""
    cur_p = ""
    for line in f:
        if 'name="Name">Vehiculos<' in line:
            in_veh = True
            continue
        if in_veh:
            if 'name="Name">Spawn_Rosewood<' in line:
                break
            if '<Item class="Model"' in line:
                cur_m = "Model"
            if '<string name="Name">' in line:
                name = line.split('>')[1].split('<')[0]
                if cur_m == "Model":
                    cur_m = name
                    print(f"Vehicle Model: {name}")
            if '<CoordinateFrame name="CFrame">' in line:
                pass
            if '<X>' in line and cur_m and cur_m != "Model":
                x = line.split('>')[1].split('<')[0]
                # check Z
            if '<Z>' in line and cur_m and cur_m != "Model":
                z = line.split('>')[1].split('<')[0]
                print(f"  {cur_m} at X={x}, Z={z}")
                cur_m = ""

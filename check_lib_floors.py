rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_lib = False
    for line in f:
        if 'name="Name">Libreria_31_45_23<' in line:
            in_lib = True
            print("Found Libreria")
            continue
        if in_lib:
            if 'name="Name">Livingroom_31_45_28<' in line:
                break
            if '<string name="Name">Piso_' in line:
                print(line.strip())

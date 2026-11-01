rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
veh_count = 0
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if 'Vehiculo_' in line:
            veh_count += 1
            if veh_count <= 5:
                print(line.strip())

print("Total Vehiculo_ instances in rbxlx:", veh_count)

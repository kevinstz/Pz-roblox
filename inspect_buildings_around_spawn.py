rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    in_edif = False
    current_building = ""
    parts = []
    building_bounds = {}
    for line in f:
        if 'name="Name">Edificios<' in line:
            in_edif = True
            continue
        if in_edif:
            if 'name="Name">Suelo_Piso_' in line or 'name="Name">Carreteras<' in line or 'name="Name">Vehiculos<' in line:
                break
            if '<string name="Name">' in line:
                val = line.split('>')[1].split('<')[0]
                if any(val.startswith(p) for p in ["Edificio_", "Casa_", "Comisaria", "Supermercado", "Juzgado", "Tienda", "Banco", "Clinica", "Escuela", "Gasolinera", "Bomberos"]):
                    current_building = val
                    if current_building not in building_bounds:
                        building_bounds[current_building] = []
            if current_building and '<X>' in line and '</X>' in line:
                try:
                    x = float(line.split('>')[1].split('<')[0])
                    building_bounds[current_building].append(x)
                except:
                    pass

print(f"Total buildings found: {len(building_bounds)}")
for b, xs in sorted(building_bounds.items()):
    if xs:
        print(f"{b}: minX={min(xs):.1f}, maxX={max(xs):.1f}, total parts={len(xs)}")

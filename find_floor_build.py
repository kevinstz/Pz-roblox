with open(r"C:\Users\julia\Downloads\pz_roblox_b42\build_map.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "Suelo_Piso" in line or "greedy" in line.lower() or "slab" in line.lower() or "floor_stack" in line:
        print(f"Line {idx+1}: {line.strip()}")

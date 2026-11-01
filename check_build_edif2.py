with open(r"C:\Users\julia\Downloads\pz_roblox_b42\build_map.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if 'edif' in line.lower() or 'building' in line.lower():
            print(f"{idx+1}: {line.rstrip()}")

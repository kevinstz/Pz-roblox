with open(r"C:\Users\julia\Downloads\pz_roblox_b42\build_map.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if 'Edificios' in line or 'bld' in line:
            if idx < 400:
                print(f"{idx+1}: {line.rstrip()}")

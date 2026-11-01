with open(r"C:\Users\julia\Downloads\pz_roblox_b42\pzlib\rbxlx.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if idx < 60:
            print(f"{idx+1}: {line.rstrip()}")

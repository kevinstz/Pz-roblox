rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

import re

def get_lib_floors_bounds():
    with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
        in_lib = False
        cur_fl = ""
        fl_parts = {}
        
        for line in f:
            if 'name="Name">Libreria_31_45_23<' in line:
                in_lib = True
                continue
            if in_lib:
                if 'name="Name">Livingroom_31_45_28<' in line:
                    break
                if '<string name="Name">Piso_' in line:
                    cur_fl = line.split('>')[1].split('<')[0]
                    fl_parts[cur_fl] = []
                if cur_fl and '<Item class="Part"' in line:
                    fl_parts[cur_fl].append(1)

    for fl, p in fl_parts.items():
        print(f"{fl}: {len(p)} parts")

get_lib_floors_bounds()

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
import re

first_grass_line = None
last_grass_line = None
with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if 'Name">blends_grassoverlays_01_' in line:
            if first_grass_line is None:
                first_grass_line = i
            last_grass_line = i

print(f"First grassoverlay: L{first_grass_line}, Last: L{last_grass_line}")

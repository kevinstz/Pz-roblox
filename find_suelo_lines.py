import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'

with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    for i in range(1, 60000):
        line = f.readline()
        if 'name="Name">Suelo<' in line or 'name="Name">Suelo_Piso' in line:
            print(f"Line {i}: {line.strip()}")

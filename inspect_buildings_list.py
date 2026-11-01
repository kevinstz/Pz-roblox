import os
import re

rbxlx = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"

edificios = []
exterior = []

current_folder = None
depth = 0

with open(rbxlx, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if '<Item class="Folder"' in line or '<Item class="Model"' in line:
            depth += 1
        elif '</Item>' in line:
            depth -= 1
        
        m_name = re.search(r'<string name="Name">(.*?)</string>', line)
        if m_name:
            name = m_name.group(1)
            if name in ["Edificios", "Exterior", "Suelos", "Vehiculos"]:
                current_folder = name
                print(f"--- FOLDER: {current_folder} ---")
            elif current_folder == "Edificios" and depth <= 4:
                if not name.startswith("Piso_"):
                    edificios.append(name)
            elif current_folder == "Exterior" and depth <= 4:
                exterior.append(name)

print(f"\nEdificios ({len(edificios)}):")
for e in edificios:
    print(" ", e)

print(f"\nExterior ({len(exterior)}):")
for ex in exterior[:30]:
    print(" ", ex)

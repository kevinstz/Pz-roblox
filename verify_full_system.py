import os
import re

p = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx'
print(f"File size: {os.path.getsize(p) / 1024 / 1024:.2f} MB")

with open(p, 'rb') as f:
    content_head = f.read(20000).decode('utf-8', errors='ignore')
    f.seek(-5000, os.SEEK_END)
    content_tail = f.read().decode('utf-8', errors='ignore')

assert '<roblox' in content_head, "Missing <roblox in head"
assert '</roblox>' in content_tail, "Missing </roblox> in tail"
print("XML root tags verified: OK")

# Count chunk models in Suelo_Piso_0
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    chunk_count = 0
    in_suelo0 = False
    for line in f:
        if 'name="Name">Suelo_Piso_0<' in line:
            in_suelo0 = True
        if in_suelo0:
            if 'name="Name">Chunk_' in line:
                chunk_count += 1
            if 'name="Name">Suelo_Piso_1<' in line:
                break

print(f"Chunks in Suelo_Piso_0: {chunk_count}")
assert chunk_count == 88, f"Expected 88 chunks, got {chunk_count}"

# Verify scripts
for scr in ['IsometricCamera', 'BuildingCutawayController', 'IsometricCursorController', 'SurvivorHUD', 'SurvivorCharacterController']:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        found = any(f'name="Name">{scr}<' in line for line in f)
        print(f"Script {scr}: {'PRESENT' if found else 'MISSING'}")
        assert found, f"Script {scr} is missing!"

# Verify Vehiculos
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    veh_found = any('name="Name">Vehiculos<' in line for line in f)
    print(f"Vehiculos folder: {'PRESENT' if veh_found else 'MISSING'}")
    assert veh_found, "Vehiculos folder is missing!"

# Verify Gabled Roofs
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    wedges = sum(1 for line in f if 'class="WedgePart"' in line)
    print(f"WedgeParts (pitched gabled roofs): {wedges}")
    assert wedges >= 21, f"Expected at least 21 WedgeParts, got {wedges}"

print("ALL INTEGRITY CHECKS PASSED 100% PERFECTLY!")

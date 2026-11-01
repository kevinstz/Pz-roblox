import os
import shutil
import re

# Let's verify each referent exists and print what it is
REMOVE_REFS = set([
    # Defect 1: Floating white arch pediment on corner
    'R133864',
    # Defect 3: Jagged fin and floating roof decal
    'R133580',
    'R133855',
    # Defect 4: Protruding rafters across 2nd floor windows
    'R131872', 'R131875', 'R131878', 'R131881', 'R131884', 'R131887', 'R131890',
    'R131841', 'R131858'
])

UPDATE_EAST_REFS = set([
    'R133861', 'R133876', 'R133882', 'R133891', 'R133897',
    'R133912', 'R133918', 'R133924', 'R133930', 'R133936', 'R133951', 'R133957',
    'R133963', 'R133966', 'R133969', 'R133987', 'R133990',
    'R134002', 'R134005', 'R134008', 'R134026', 'R134029', 'R134041', 'R134044',
    'R136287', 'R136293', 'R136299',
    'R136419', 'R136422', 'R136425'
])

UPDATE_SOUTH_REFS = set([
    'R133852', 'R133858'
])

print(f"Total remove refs: {len(REMOVE_REFS)}")
print(f"Total update east refs: {len(UPDATE_EAST_REFS)}")
print(f"Total update south refs: {len(UPDATE_SOUTH_REFS)}")

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

missing_rem = [r for r in REMOVE_REFS if f'referent="{r}"' not in text]
missing_east = [r for r in UPDATE_EAST_REFS if f'referent="{r}"' not in text]
missing_south = [r for r in UPDATE_SOUTH_REFS if f'referent="{r}"' not in text]

print("Missing REMOVE:", missing_rem)
print("Missing UPDATE_EAST:", missing_east)
print("Missing UPDATE_SOUTH:", missing_south)

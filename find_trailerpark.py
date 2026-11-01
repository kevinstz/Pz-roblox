import os
import sys

ROOT = r"C:\Users\julia\Downloads\pz_roblox_b42"
sys.path.insert(0, ROOT)
from pzlib.assets import MEDIA

# Let's inspect lot files in Muldraugh, KY
MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
print("Scanning for lot files in MAPDIR...")
files = [f for f in os.listdir(MAPDIR) if f.endswith('.lotheader')]
print(f"Total lotheader files: {len(files)}")

# Look for coordinates around Rosewood (Rosewood is around cell 26..28, 38..40, or 31..32, 45..46)
rosewood_cells = []
for f in files:
    # world_X_Y.lotheader
    parts = f.replace('.lotheader', '').split('_')
    if len(parts) == 3:
        cx, cy = int(parts[1]), int(parts[2])
        if 25 <= cx <= 35 and 38 <= cy <= 48:
            rosewood_cells.append((cx, cy))

print("Rosewood area cells:", sorted(rosewood_cells))

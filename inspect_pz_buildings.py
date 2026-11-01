import sys
import os

ROOT = r"C:\Users\julia\Downloads\pz_roblox_b42"
sys.path.insert(0, ROOT)
from pzlib.lot import load_region
from pzlib.assets import MEDIA

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)
print(f"Loaded {len(rooms)} rooms across region {REGION}")

# Group rooms by building
buildings = {}
for rm in rooms:
    key = None
    for (cx, cy), hdr in headers.items():
        if rm in hdr.rooms:
            key = (cx, cy, rm.building)
            break
    if key not in buildings:
        buildings[key] = []
    buildings[key].append(rm)

print(f"Found {len(buildings)} buildings:")
for key, rms in sorted(buildings.items(), key=lambda kv: str(kv[0])):
    room_names = [r.name for r in rms]
    # compute bounding box of building in world coordinates
    all_rects = [rect for r in rms for rect in r.rects]
    min_rx = min(r[0] for r in all_rects)
    max_rx = max(r[0] + r[2] for r in all_rects)
    min_ry = min(r[1] for r in all_rects)
    max_ry = max(r[1] + r[3] for r in all_rects)
    levels = set(r.level for r in rms)
    print(f"  Building {key}: {len(rms)} rooms: {set(room_names)}, levels={levels}, X=[{min_rx}..{max_rx}], Y=[{min_ry}..{max_ry}]")

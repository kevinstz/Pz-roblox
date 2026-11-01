import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex
import os

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
REGION = (8040, 11585, 8165, 11760)
x0, y0, x1, y1 = REGION

squares, rooms, headers = load_region(MAPDIR, x0, y0, x1, y1)
props = load_all_tiles()
packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

WALL_FLAGS = {'WallN', 'WallW', 'WallNW', 'DoorWallN', 'DoorWallW', 'WallSE'}
_sprites = {}
def sprite(name):
    if name not in _sprites:
        _sprites[name] = packs.sprite(name)
    return _sprites[name]

def is_floor_layer(name):
    p = props.get(name, {})
    if 'solidfloor' in p or 'FloorOverlay' in p:
        return True
    if any(k in p for k in WALL_FLAGS) or 'doorN' in p or 'doorW' in p or 'windowN' in p or 'windowW' in p:
        return False
    if 'attachedFloor' in p or 'IsFloorAttached' in p or name.startswith(('blends_', 'floors_', 'overlay_grime_floor',
                                                                           'street_trafficlines', 'd_streetcracks', 'd_generic')):
        img = sprite(name)
        if img is not None:
            bb = img.getbbox()
            return bb is not None and bb[1] >= 186
    return False

# Now simulate floor_stack
missing = []
for y in range(11703, 11720):
    row = []
    for x in range(8053, 8066):
        names = squares.get((x, y, 0), [])
        layers = []
        for n in names:
            if is_floor_layer(n) and sprite(n) is not None:
                layers.append(n)
            else:
                break
        if not layers:
            row.append("MISS")
            missing.append((x, y, names))
        else:
            row.append(f"{len(layers)}ly")
    print(f"y={y}: " + " ".join(row))

print(f"\nTotal missing in this box: {len(missing)}")
for m in missing[:10]:
    print("Missing:", m)

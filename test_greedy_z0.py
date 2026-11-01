import sys, os
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex
from pzlib.iso import floor_image

props = load_all_tiles()
packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

WALL_FLAGS = {'WallN', 'WallW', 'WallNW', 'DoorWallN', 'DoorWallW', 'WallSE'}
_sprites = {}
def sprite(name):
    if name not in _sprites:
        _sprites[name] = packs.sprite(name)
    return _sprites[name]

_floorlike = {}
def is_floor_layer(name):
    if name in _floorlike:
        return _floorlike[name]
    p = props.get(name, {})
    res = False
    if 'solidfloor' in p or 'FloorOverlay' in p:
        res = True
    elif any(k in p for k in WALL_FLAGS) or 'doorN' in p or 'doorW' in p or 'windowN' in p or 'windowW' in p:
        res = False
    elif 'attachedFloor' in p or 'IsFloorAttached' in p or name.startswith(('blends_', 'floors_', 'overlay_grime_floor',
                                                                           'street_trafficlines', 'd_streetcracks', 'd_generic',
                                                                           'street_curbs')):
        img = sprite(name)
        if img is not None:
            bb = img.getbbox()
            res = bb is not None and bb[1] >= 180
    _floorlike[name] = res
    return res

squares, rooms, headers = load_region(os.path.join(MEDIA, 'maps', 'Muldraugh, KY'), 8040, 11585, 8165, 11760)

floor_stack = {}
for (x, y, z), names in squares.items():
    if z == 0:
        layers = []
        for n in names:
            if is_floor_layer(n) and sprite(n) is not None:
                layers.append(n)
            else:
                break
        if layers:
            floor_stack[(x, y)] = tuple(layers)

print(f"Total z=0 floor squares: {len(floor_stack)}")
unique_stacks = set(floor_stack.values())
print(f"Total unique stacks: {len(unique_stacks)}")

# Test greedy merging
used = set()
merged_parts = []
for (x, y) in sorted(floor_stack.keys(), key=lambda a: (a[1], a[0])):
    if (x, y) in used:
        continue
    key = floor_stack[(x, y)]
    w = 1
    while (x + w, y) in floor_stack and (x + w, y) not in used and floor_stack[(x + w, y)] == key:
        w += 1
    h = 1
    while True:
        row_ok = all((x + i, y + h) in floor_stack and (x + i, y + h) not in used and floor_stack[(x + i, y + h)] == key
                     for i in range(w))
        if not row_ok:
            break
        h += 1
    for i in range(w):
        for j in range(h):
            used.add((x + i, y + j))
    merged_parts.append((x, y, w, h, key))

print(f"Merged into {len(merged_parts)} parts (from {len(floor_stack)} squares)")

import sys
import collections
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex

props = load_all_tiles()
packs = PackIndex(['Tiles2x.floor.pack', 'Tiles2x.pack', 'Overlays2x.floor.pack', 'Overlays2x.pack',
                   'B42ChunkCaching2x.floor.pack', 'B42ChunkCaching2x.pack', 'JumboTrees2x.pack'])

_sprites = {}
def sprite(name):
    if name not in _sprites:
        _sprites[name] = packs.sprite(name)
    return _sprites[name]

WALL_FLAGS = {'WallN', 'WallW', 'WallNW', 'DoorWallN', 'DoorWallW', 'WallSE'}
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

MAPDIR = rf"{MEDIA}\maps\Muldraugh, KY"
squares, rooms, headers = load_region(MAPDIR, 8040, 11585, 8165, 11760)

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

CHUNK_SIZE = 16
chunks = collections.defaultdict(dict)
for (x, y), key in floor_stack.items():
    ch_x = (x - 8040) // CHUNK_SIZE
    ch_y = (y - 11585) // CHUNK_SIZE
    chunks[(ch_x, ch_y)][(x, y)] = key

print(f"Total spatial chunks ({CHUNK_SIZE}x{CHUNK_SIZE} tiles = {CHUNK_SIZE*3}x{CHUNK_SIZE*3} studs): {len(chunks)}")

total_merged_parts = 0
chunk_part_counts = []

for ch_idx, ch_squares in sorted(chunks.items()):
    used = set()
    ch_parts = []
    for (x, y) in sorted(ch_squares.keys(), key=lambda a: (a[1], a[0])):
        if (x, y) in used:
            continue
        key = ch_squares[(x, y)]
        w = 1
        while (x + w, y) in ch_squares and (x + w, y) not in used and ch_squares[(x + w, y)] == key:
            w += 1
        h = 1
        while True:
            row_ok = all((x + i, y + h) in ch_squares and (x + i, y + h) not in used and ch_squares[(x + i, y + h)] == key
                         for i in range(w))
            if not row_ok:
                break
            h += 1
        for i in range(w):
            for j in range(h):
                used.add((x + i, y + j))
        ch_parts.append((x, y, w, h, key))
    total_merged_parts += len(ch_parts)
    chunk_part_counts.append(len(ch_parts))

print(f"Total merged parts across all chunks: {total_merged_parts}")
print(f"Min parts in a chunk: {min(chunk_part_counts)}, Max: {max(chunk_part_counts)}, Avg: {sum(chunk_part_counts)/len(chunk_part_counts):.1f}")

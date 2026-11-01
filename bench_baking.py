import sys, os, time
from PIL import Image
import numpy as np

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

unique_stacks = list(set(floor_stack.values()))

t0 = time.time()
_cache = {}
def bake_stack(layers):
    base_spr = sprite(layers[0])
    base_img = floor_image(base_spr).convert('RGBA')
    arr = np.array(base_img)
    mask = arr[:, :, 3] < 200
    if mask.any():
        valid = arr[:, :, 3] >= 200
        if valid.any():
            mean_rgb = arr[valid, :3].mean(axis=0).astype(np.uint8)
        else:
            mean_rgb = np.array([76, 115, 48], dtype=np.uint8)
        arr[mask, :3] = mean_rgb
        arr[mask, 3] = 255
        base_img = Image.fromarray(arr)
    
    for n in layers[1:]:
        spr = sprite(n)
        if spr is not None:
            ov = floor_image(spr).convert('RGBA')
            base_img = Image.alpha_composite(base_img, ov)
    return base_img

for s in unique_stacks[:200]:
    img = bake_stack(s)

dt = time.time() - t0
print(f"Baked 200 unique textures in {dt:.2f}s ({dt/200*1000:.1f}ms each)")
print(f"Estimated time for all {len(unique_stacks)} textures: {dt/200*len(unique_stacks):.2f}s")

import sys, os
from collections import Counter

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex

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

unique_stacks = set(floor_stack.values())

def get_material_and_color(base_name):
    p = props.get(base_name, {})
    fmat = p.get('FloorMaterial', '')
    
    if base_name.startswith(('blends_natural_', 'floors_exterior_natural_')):
        if 'Sand' in fmat or 'sand' in base_name.lower():
            # Material.Sand = 1296
            return 1296, (195, 175, 135)
        elif 'Dirt' in fmat or 'dirt' in base_name.lower():
            # Material.Ground = 1312
            return 1312, (90, 68, 42)
        else: # Grass
            # Material.Grass = 1280
            return 1280, (76, 115, 48) # Rich Kentucky grass green!
    elif base_name.startswith(('blends_street_', 'floors_exterior_street_', 'street_curbs_')):
        if base_name in ['blends_street_01_48', 'blends_street_01_49', 'blends_street_01_50',
                         'blends_street_01_51', 'blends_street_01_52', 'blends_street_01_53',
                         'blends_street_01_54', 'blends_street_01_55'] or 'tilesandstone' in base_name:
            # Sidewalk: Material.Concrete = 816
            return 816, (142, 140, 135)
        else:
            # Road / Asphalt: Material.Asphalt = 1376
            return 1376, (56, 56, 60)
    elif base_name.startswith('floors_interior_'):
        if 'wood' in base_name.lower():
            return 528, (160, 115, 75) # WoodPlanks = 528
        elif 'carpet' in base_name.lower():
            return 1312, (120, 110, 100) # Fabric = 1312
        else:
            return 816, (150, 150, 150) # Concrete / Tile
    else:
        return 272, (140, 140, 140) # SmoothPlastic

mat_counts = Counter()
for s in unique_stacks:
    mat, col = get_material_and_color(s[0])
    mat_counts[mat] += 1

print("Material counts across unique stacks:", mat_counts)

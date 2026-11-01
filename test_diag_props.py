import sys
sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
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

names = ['blends_street_01_70', 'street_curbs_01_blend_gravel_27', 'street_curbs_01_diag_1']
for n in names:
    p = props.get(n, {})
    spr = sprite(n)
    ifl = is_floor_layer(n)
    print(f"{n:<35}: props={p}, spr={'Found' if spr else 'None'}, is_floor_layer={ifl}")

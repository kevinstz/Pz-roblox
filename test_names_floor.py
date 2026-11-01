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
            print(f"  {name}: bb={bb}")
            return bb is not None and bb[1] >= 186
    return False

names = ['blends_street_01_69', 'blends_street_01_58', 'overlay_grime_floor_01_37', 'street_curbs_01_11']
for n in names:
    res = is_floor_layer(n)
    print(f"{n:<30} -> is_floor_layer = {res}")

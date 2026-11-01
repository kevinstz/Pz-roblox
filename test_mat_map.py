import sys
import os
import hashlib
import time
from collections import defaultdict
from PIL import Image
import numpy as np

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex
from pzlib.iso import floor_image, S6

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

OUT_TEX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"
STUDIO_TEX = r"C:\Users\julia\AppData\Local\Roblox\Versions\version-7062aec9dbe74b14\content\pz42"

def get_material_and_color(base_name):
    p = props.get(base_name, {})
    fmat = p.get('FloorMaterial', '')
    
    if base_name.startswith(('blends_natural_', 'floors_exterior_natural_')):
        if 'Sand' in fmat or 'sand' in base_name.lower():
            # Material.Sand = 1296
            return 1296, 4291083944 # (195, 175, 135)
        elif 'Dirt' in fmat or 'dirt' in base_name.lower():
            # Material.Ground = 1312
            return 1312, 4284104468 # (90, 68, 42)
        else: # Grass
            # Material.Grass = 1280
            return 1280, 4284122216 # (76, 115, 48) - vibrant Kentucky green!
    elif base_name.startswith(('blends_street_', 'floors_exterior_street_', 'street_curbs_')):
        if base_name in ['blends_street_01_48', 'blends_street_01_49', 'blends_street_01_50',
                         'blends_street_01_51', 'blends_street_01_52', 'blends_street_01_53',
                         'blends_street_01_54', 'blends_street_01_55'] or 'tilesandstone' in base_name:
            # Sidewalk: Material.Concrete = 816
            return 816, 4288649348 # (142, 140, 135)
        else:
            # Road / Asphalt: Material.Asphalt = 1376
            return 1376, 4281874236 # (56, 56, 60)
    elif base_name.startswith('floors_interior_'):
        if 'wood' in base_name.lower():
            return 512, 4286866236 # WoodPlanks
        elif 'carpet' in base_name.lower():
            return 1360, 4285558896 # Fabric
        else:
            return 816, 4286808440 # Concrete / Tile
    else:
        return 272, 4286808440 # SmoothPlastic

print("Testing material and color mapping:")
for test_n in ['blends_natural_01_16', 'blends_natural_01_64', 'blends_street_01_48', 'blends_street_01_70', 'floors_interior_tilesandwood_01_1']:
    mat, col = get_material_and_color(test_n)
    print(f"  {test_n:<35}: mat={mat}, col={col}")

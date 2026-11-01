import collections
import hashlib
import io
import os
import shutil
import sys
import time
from PIL import Image
import numpy as np

print("=== Iniciando aplicacion definitiva de Suelo_Piso_0 con Chunks Espaciales ===")
t_start = time.time()

sys.path.append(r'C:\Users\julia\Downloads\pz_roblox_b42')
from pzlib.lot import load_region
from pzlib.assets import MEDIA, load_all_tiles, PackIndex
from pzlib.iso import floor_image

OUT_RBXLX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
BAK_RBXLX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_before_chunking"
TMP_RBXLX = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.tmp"
OUT_TEX_DIR = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\textures"
STUDIO_TEX_DIR = r"C:\Users\julia\AppData\Local\Roblox\Versions\version-7062aec9dbe74b14\content\pz42"

# Crear respaldo de seguridad antes de proceder
if not os.path.exists(BAK_RBXLX):
    print("Creando respaldo previo de PZ_Rosewood.rbxlx...")
    shutil.copy2(OUT_RBXLX, BAK_RBXLX)

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

MAPDIR = os.path.join(MEDIA, 'maps', 'Muldraugh, KY')
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

print(f"Cuadros de suelo en z=0: {len(floor_stack)}")

unique_stacks = sorted(list(set(floor_stack.values())), key=lambda s: (len(s), s))
print(f"Pilas unicas de capas: {len(unique_stacks)}")

stack_to_url = {}
for s in unique_stacks:
    base_spr = sprite(s[0])
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
    
    for n in s[1:]:
        spr = sprite(n)
        if spr is not None:
            ov = floor_image(spr).convert('RGBA')
            base_img = Image.alpha_composite(base_img, ov)
            
    buf = io.BytesIO()
    base_img.save(buf, 'PNG', optimize=False)
    data = buf.getvalue()
    h = hashlib.sha1(data).hexdigest()[:20]
    
    tex_path = os.path.join(OUT_TEX_DIR, h + '.png')
    if not os.path.exists(tex_path):
        with open(tex_path, 'wb') as f:
            f.write(data)
    studio_path = os.path.join(STUDIO_TEX_DIR, h + '.png')
    if not os.path.exists(studio_path):
        with open(studio_path, 'wb') as f:
            f.write(data)
    stack_to_url[s] = f"rbxasset://pz42/{h}.png"

def get_material_and_color(base_name):
    p = props.get(base_name, {})
    fmat = p.get('FloorMaterial', '')
    if base_name.startswith(('blends_natural_', 'floors_exterior_natural_')):
        if 'Sand' in fmat or 'sand' in base_name.lower():
            return 1296, (195, 175, 135)
        elif 'Dirt' in fmat or 'dirt' in base_name.lower():
            return 1312, (90, 68, 42)
        else:
            return 1280, (76, 115, 48)
    elif base_name.startswith(('blends_street_', 'floors_exterior_street_', 'street_curbs_')):
        if base_name in ['blends_street_01_48', 'blends_street_01_49', 'blends_street_01_50',
                         'blends_street_01_51', 'blends_street_01_52', 'blends_street_01_53',
                         'blends_street_01_54', 'blends_street_01_55'] or 'tilesandstone' in base_name:
            return 816, (142, 140, 135)
        else:
            return 1376, (56, 56, 60)
    elif base_name.startswith('floors_interior_'):
        if 'wood' in base_name.lower():
            return 528, (160, 115, 75)
        elif 'carpet' in base_name.lower():
            return 1312, (120, 110, 100)
        else:
            return 816, (150, 150, 150)
    elif 'carpet' in base_name.lower():
        return 1312, (120, 110, 100)
    elif any(k in base_name.lower() for k in ['tiles', 'stone', 'industry', 'diner', 'shop']):
        return 816, (150, 150, 150)
    else:
        return 272, (140, 140, 140)

# Agrupar en Chunks espaciales de 16x16 tiles (48x48 studs)
CHUNK_SIZE = 16
chunks = collections.defaultdict(dict)
for (x, y), key in floor_stack.items():
    ch_x = (x - 8040) // CHUNK_SIZE
    ch_y = (y - 11585) // CHUNK_SIZE
    chunks[(ch_x, ch_y)][(x, y)] = key

OX = (8040 + 8165) / 2.0 # 8102.5
OY = (11585 + 11760) / 2.0 # 11672.5
TILE = 3.0

print(f"Generando XML de Suelo_Piso_0 con {len(chunks)} chunks espaciales...")

lines = []
lines.append('\t\t\t\t<Item class="Folder" referent="R739">\n')
lines.append('\t\t\t\t\t<Properties>\n')
lines.append('\t\t\t\t\t\t<BinaryString name="AttributesSerialize"></BinaryString>\n')
lines.append('\t\t\t\t\t\t<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>\n')
lines.append('\t\t\t\t\t\t<bool name="DefinesCapabilities">false</bool>\n')
lines.append('\t\t\t\t\t\t<UniqueId name="HistoryId">00000000000000000000000000000000</UniqueId>\n')
lines.append('\t\t\t\t\t\t<string name="Name">Suelo_Piso_0</string>\n')
lines.append('\t\t\t\t\t\t<BinaryString name="SerializedOverrides"></BinaryString>\n')
lines.append('\t\t\t\t\t\t<int64 name="SourceAssetId">-1</int64>\n')
lines.append('\t\t\t\t\t\t<SharedString name="Tags">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>\n')
lines.append('\t\t\t\t\t\t<UniqueId name="UniqueId">f7000000000000000000000000000739</UniqueId>\n')
lines.append('\t\t\t\t\t</Properties>\n')

ref_counter = 300000
global_part_idx = 0

for ch_idx, ((ch_x, ch_y), ch_squares) in enumerate(sorted(chunks.items())):
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

    pz_min_x = 8040 + ch_x * CHUNK_SIZE
    pz_max_x = min(8165, pz_min_x + CHUNK_SIZE - 1)
    pz_min_y = 11585 + ch_y * CHUNK_SIZE
    pz_max_y = min(11760, pz_min_y + CHUNK_SIZE - 1)
    
    c_world_x = ((pz_min_x + pz_max_x) / 2.0 + 0.5 - OX) * TILE
    c_world_z = ((pz_min_y + pz_max_y) / 2.0 + 0.5 - OY) * TILE
    
    ch_ref = ref_counter
    ref_counter += 1
    ch_uid = f"f7000000000000000010{ch_idx:012x}"
    
    c_wx_s = f"{c_world_x:.4f}".rstrip('0').rstrip('.') if c_world_x != 0 else '0'
    c_wz_s = f"{c_world_z:.4f}".rstrip('0').rstrip('.') if c_world_z != 0 else '0'

    lines.append(f'\t\t\t\t\t<Item class="Model" referent="R{ch_ref}">\n')
    lines.append('\t\t\t\t\t\t<Properties>\n')
    lines.append('\t\t\t\t\t\t\t<token name="LevelOfDetail">0</token>\n')
    lines.append('\t\t\t\t\t\t\t<CoordinateFrame name="ModelMeshCFrame">\n')
    lines.append('\t\t\t\t\t\t\t\t<X>0</X><Y>0</Y><Z>0</Z>\n')
    lines.append('\t\t\t\t\t\t\t\t<R00>1</R00><R01>0</R01><R02>0</R02>\n')
    lines.append('\t\t\t\t\t\t\t\t<R10>0</R10><R11>1</R11><R12>0</R12>\n')
    lines.append('\t\t\t\t\t\t\t\t<R20>0</R20><R21>0</R21><R22>1</R22>\n')
    lines.append('\t\t\t\t\t\t\t</CoordinateFrame>\n')
    lines.append('\t\t\t\t\t\t\t<SharedString name="ModelMeshData">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>\n')
    lines.append('\t\t\t\t\t\t\t<Vector3 name="ModelMeshSize"><X>0</X><Y>0</Y><Z>0</Z></Vector3>\n')
    lines.append('\t\t\t\t\t\t\t<token name="ModelStreamingMode">0</token>\n')
    lines.append('\t\t\t\t\t\t\t<bool name="NeedsPivotMigration">false</bool>\n')
    lines.append('\t\t\t\t\t\t\t<Ref name="PrimaryPart">null</Ref>\n')
    lines.append('\t\t\t\t\t\t\t<float name="ScaleFactor">1</float>\n')
    lines.append('\t\t\t\t\t\t\t<SharedString name="SlimHash">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>\n')
    lines.append('\t\t\t\t\t\t\t<OptionalCoordinateFrame name="WorldPivotData">\n')
    lines.append('\t\t\t\t\t\t\t\t<CFrame>\n')
    lines.append(f'\t\t\t\t\t\t\t\t\t<X>{c_wx_s}</X><Y>-1.5</Y><Z>{c_wz_s}</Z>\n')
    lines.append('\t\t\t\t\t\t\t\t\t<R00>1</R00><R01>0</R01><R02>0</R02>\n')
    lines.append('\t\t\t\t\t\t\t\t\t<R10>0</R10><R11>1</R11><R12>0</R12>\n')
    lines.append('\t\t\t\t\t\t\t\t\t<R20>0</R20><R21>0</R21><R22>1</R22>\n')
    lines.append('\t\t\t\t\t\t\t\t</CFrame>\n')
    lines.append('\t\t\t\t\t\t\t</OptionalCoordinateFrame>\n')
    lines.append('\t\t\t\t\t\t\t<BinaryString name="AttributesSerialize"></BinaryString>\n')
    lines.append('\t\t\t\t\t\t\t<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>\n')
    lines.append('\t\t\t\t\t\t\t<bool name="DefinesCapabilities">false</bool>\n')
    lines.append('\t\t\t\t\t\t\t<UniqueId name="HistoryId">00000000000000000000000000000000</UniqueId>\n')
    lines.append(f'\t\t\t\t\t\t\t<string name="Name">Chunk_{ch_x}_{ch_y}</string>\n')
    lines.append('\t\t\t\t\t\t\t<BinaryString name="SerializedOverrides"></BinaryString>\n')
    lines.append('\t\t\t\t\t\t\t<int64 name="SourceAssetId">-1</int64>\n')
    lines.append('\t\t\t\t\t\t\t<SharedString name="Tags">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>\n')
    lines.append(f'\t\t\t\t\t\t\t<UniqueId name="UniqueId">{ch_uid}</UniqueId>\n')
    lines.append('\t\t\t\t\t\t</Properties>\n')

    for (x, y, w, h, key) in ch_parts:
        ref_part = ref_counter
        ref_tex = ref_counter + 1
        ref_counter += 2
        
        uid_part = f"f7000000000000000001{global_part_idx:012x}"
        uid_tex  = f"f7000000000000000002{global_part_idx:012x}"
        global_part_idx += 1
        
        cx = (x + w / 2.0 - OX) * TILE
        cz = (y + h / 2.0 - OY) * TILE
        sx = w * TILE
        sy = 3.0
        sz = h * TILE
        
        mat_token, col_rgb = get_material_and_color(key[0])
        r, g, b = col_rgb
        c_uint32 = 0xFF000000 | (r << 16) | (g << 8) | b
        tex_url = stack_to_url[key]
        part_name = "Suelo|" + key[0]
        
        cx_s = f"{cx:.4f}".rstrip('0').rstrip('.') if cx != 0 else '0'
        cz_s = f"{cz:.4f}".rstrip('0').rstrip('.') if cz != 0 else '0'
        sx_s = f"{sx:.4f}".rstrip('0').rstrip('.') if sx != 0 else '0'
        sz_s = f"{sz:.4f}".rstrip('0').rstrip('.') if sz != 0 else '0'

        part_xml = f"""\t\t\t\t\t\t<Item class="Part" referent="R{ref_part}">
\t\t\t\t\t\t\t<Properties>
\t\t\t\t\t\t\t\t<token name="shape">1</token>
\t\t\t\t\t\t\t\t<token name="formFactorRaw">1</token>
\t\t\t\t\t\t\t\t<bool name="Anchored">true</bool>
\t\t\t\t\t\t\t\t<bool name="AudioCanCollide">true</bool>
\t\t\t\t\t\t\t\t<float name="BackParamA">-0.5</float>
\t\t\t\t\t\t\t\t<float name="BackParamB">0.5</float>
\t\t\t\t\t\t\t\t<token name="BackSurface">0</token>
\t\t\t\t\t\t\t\t<token name="BackSurfaceInput">0</token>
\t\t\t\t\t\t\t\t<float name="BottomParamA">-0.5</float>
\t\t\t\t\t\t\t\t<float name="BottomParamB">0.5</float>
\t\t\t\t\t\t\t\t<token name="BottomSurface">0</token>
\t\t\t\t\t\t\t\t<token name="BottomSurfaceInput">0</token>
\t\t\t\t\t\t\t\t<CoordinateFrame name="CFrame">
\t\t\t\t\t\t\t\t\t<X>{cx_s}</X>
\t\t\t\t\t\t\t\t\t<Y>-1.5</Y>
\t\t\t\t\t\t\t\t\t<Z>{cz_s}</Z>
\t\t\t\t\t\t\t\t\t<R00>1</R00>
\t\t\t\t\t\t\t\t\t<R01>0</R01>
\t\t\t\t\t\t\t\t\t<R02>0</R02>
\t\t\t\t\t\t\t\t\t<R10>0</R10>
\t\t\t\t\t\t\t\t\t<R11>1</R11>
\t\t\t\t\t\t\t\t\t<R12>0</R12>
\t\t\t\t\t\t\t\t\t<R20>0</R20>
\t\t\t\t\t\t\t\t\t<R21>0</R21>
\t\t\t\t\t\t\t\t\t<R22>1</R22>
\t\t\t\t\t\t\t\t</CoordinateFrame>
\t\t\t\t\t\t\t\t<bool name="CanCollide">true</bool>
\t\t\t\t\t\t\t\t<bool name="CanQuery">true</bool>
\t\t\t\t\t\t\t\t<bool name="CanTouch">true</bool>
\t\t\t\t\t\t\t\t<bool name="CastShadow">true</bool>
\t\t\t\t\t\t\t\t<string name="CollisionGroup">Default</string>
\t\t\t\t\t\t\t\t<int name="CollisionGroupId">0</int>
\t\t\t\t\t\t\t\t<Color3uint8 name="Color3uint8">{c_uint32}</Color3uint8>
\t\t\t\t\t\t\t\t<PhysicalProperties name="CustomPhysicalProperties">
\t\t\t\t\t\t\t\t\t<CustomPhysics>false</CustomPhysics>
\t\t\t\t\t\t\t\t</PhysicalProperties>
\t\t\t\t\t\t\t\t<bool name="EnableFluidForces">true</bool>
\t\t\t\t\t\t\t\t<float name="FrontParamA">-0.5</float>
\t\t\t\t\t\t\t\t<float name="FrontParamB">0.5</float>
\t\t\t\t\t\t\t\t<token name="FrontSurface">0</token>
\t\t\t\t\t\t\t\t<token name="FrontSurfaceInput">0</token>
\t\t\t\t\t\t\t\t<float name="LeftParamA">-0.5</float>
\t\t\t\t\t\t\t\t<float name="LeftParamB">0.5</float>
\t\t\t\t\t\t\t\t<token name="LeftSurface">0</token>
\t\t\t\t\t\t\t\t<token name="LeftSurfaceInput">0</token>
\t\t\t\t\t\t\t\t<bool name="Locked">false</bool>
\t\t\t\t\t\t\t\t<bool name="Massless">false</bool>
\t\t\t\t\t\t\t\t<token name="Material">{mat_token}</token>
\t\t\t\t\t\t\t\t<string name="MaterialVariantSerialized"></string>
\t\t\t\t\t\t\t\t<CoordinateFrame name="PivotOffset">
\t\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t\t<Z>0</Z>
\t\t\t\t\t\t\t\t\t<R00>1</R00>
\t\t\t\t\t\t\t\t\t<R01>0</R01>
\t\t\t\t\t\t\t\t\t<R02>0</R02>
\t\t\t\t\t\t\t\t\t<R10>0</R10>
\t\t\t\t\t\t\t\t\t<R11>1</R11>
\t\t\t\t\t\t\t\t\t<R12>0</R12>
\t\t\t\t\t\t\t\t\t<R20>0</R20>
\t\t\t\t\t\t\t\t\t<R21>0</R21>
\t\t\t\t\t\t\t\t\t<R22>1</R22>
\t\t\t\t\t\t\t\t</CoordinateFrame>
\t\t\t\t\t\t\t\t<float name="Reflectance">0</float>
\t\t\t\t\t\t\t\t<float name="RightParamA">-0.5</float>
\t\t\t\t\t\t\t\t<float name="RightParamB">0.5</float>
\t\t\t\t\t\t\t\t<token name="RightSurface">0</token>
\t\t\t\t\t\t\t\t<token name="RightSurfaceInput">0</token>
\t\t\t\t\t\t\t\t<int name="RootPriority">0</int>
\t\t\t\t\t\t\t\t<Vector3 name="RotVelocity">
\t\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t\t<Z>0</Z>
\t\t\t\t\t\t\t\t</Vector3>
\t\t\t\t\t\t\t\t<float name="TopParamA">-0.5</float>
\t\t\t\t\t\t\t\t<float name="TopParamB">0.5</float>
\t\t\t\t\t\t\t\t<token name="TopSurface">0</token>
\t\t\t\t\t\t\t\t<token name="TopSurfaceInput">0</token>
\t\t\t\t\t\t\t\t<float name="Transparency">0</float>
\t\t\t\t\t\t\t\t<Vector3 name="Velocity">
\t\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t\t<Z>0</Z>
\t\t\t\t\t\t\t\t</Vector3>
\t\t\t\t\t\t\t\t<Vector3 name="size">
\t\t\t\t\t\t\t\t\t<X>{sx_s}</X>
\t\t\t\t\t\t\t\t\t<Y>3</Y>
\t\t\t\t\t\t\t\t\t<Z>{sz_s}</Z>
\t\t\t\t\t\t\t\t</Vector3>
\t\t\t\t\t\t\t\t<BinaryString name="AttributesSerialize"></BinaryString>
\t\t\t\t\t\t\t\t<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>
\t\t\t\t\t\t\t\t<bool name="DefinesCapabilities">false</bool>
\t\t\t\t\t\t\t\t<UniqueId name="HistoryId">00000000000000000000000000000000</UniqueId>
\t\t\t\t\t\t\t\t<string name="Name">{part_name}</string>
\t\t\t\t\t\t\t\t<BinaryString name="SerializedOverrides"></BinaryString>
\t\t\t\t\t\t\t\t<int64 name="SourceAssetId">-1</int64>
\t\t\t\t\t\t\t\t<SharedString name="Tags">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>
\t\t\t\t\t\t\t\t<UniqueId name="UniqueId">{uid_part}</UniqueId>
\t\t\t\t\t\t\t</Properties>
\t\t\t\t\t\t\t<Item class="Texture" referent="R{ref_tex}">
\t\t\t\t\t\t\t\t<Properties>
\t\t\t\t\t\t\t\t\t<float name="OffsetStudsU">0</float>
\t\t\t\t\t\t\t\t\t<float name="OffsetStudsV">0</float>
\t\t\t\t\t\t\t\t\t<float name="StudsPerTileU">3</float>
\t\t\t\t\t\t\t\t\t<float name="StudsPerTileV">3</float>
\t\t\t\t\t\t\t\t\t<bool name="AutoLocalize">true</bool>
\t\t\t\t\t\t\t\t\t<Color3 name="Color3">
\t\t\t\t\t\t\t\t\t\t<R>1</R>
\t\t\t\t\t\t\t\t\t\t<G>1</G>
\t\t\t\t\t\t\t\t\t\t<B>1</B>
\t\t\t\t\t\t\t\t\t</Color3>
\t\t\t\t\t\t\t\t\t<Content name="EmissiveMaskContent">
\t\t\t\t\t\t\t\t\t\t<null></null>
\t\t\t\t\t\t\t\t\t</Content>
\t\t\t\t\t\t\t\t\t<float name="EmissiveStrength">1</float>
\t\t\t\t\t\t\t\t\t<Color3 name="EmissiveTint">
\t\t\t\t\t\t\t\t\t\t<R>1</R>
\t\t\t\t\t\t\t\t\t\t<G>1</G>
\t\t\t\t\t\t\t\t\t\t<B>1</B>
\t\t\t\t\t\t\t\t\t</Color3>
\t\t\t\t\t\t\t\t\t<Content name="MetalnessMap"><null></null></Content>
\t\t\t\t\t\t\t\t\t<Content name="NormalMap"><null></null></Content>
\t\t\t\t\t\t\t\t\t<token name="ResampleMode">0</token>
\t\t\t\t\t\t\t\t\t<float name="Rotation">0</float>
\t\t\t\t\t\t\t\t\t<Content name="RoughnessMap"><null></null></Content>
\t\t\t\t\t\t\t\t\t<Content name="Texture"><url>{tex_url}</url></Content>
\t\t\t\t\t\t\t\t\t<Content name="TexturePack"><null></null></Content>
\t\t\t\t\t\t\t\t\t<string name="TexturePackMetadata"></string>
\t\t\t\t\t\t\t\t\t<float name="Transparency">0</float>
\t\t\t\t\t\t\t\t\t<Vector2 name="UVOffset">
\t\t\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t\t</Vector2>
\t\t\t\t\t\t\t\t\t<Vector2 name="UVScale">
\t\t\t\t\t\t\t\t\t\t<X>1</X>
\t\t\t\t\t\t\t\t\t\t<Y>1</Y>
\t\t\t\t\t\t\t\t\t</Vector2>
\t\t\t\t\t\t\t\t\t<int name="ZIndex">1</int>
\t\t\t\t\t\t\t\t\t<token name="Face">1</token>
\t\t\t\t\t\t\t\t\t<BinaryString name="AttributesSerialize"></BinaryString>
\t\t\t\t\t\t\t\t\t<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>
\t\t\t\t\t\t\t\t\t<bool name="DefinesCapabilities">false</bool>
\t\t\t\t\t\t\t\t\t<UniqueId name="HistoryId">00000000000000000000000000000000</UniqueId>
\t\t\t\t\t\t\t\t\t<string name="Name">Texture</string>
\t\t\t\t\t\t\t\t\t<BinaryString name="SerializedOverrides"></BinaryString>
\t\t\t\t\t\t\t\t\t<int64 name="SourceAssetId">-1</int64>
\t\t\t\t\t\t\t\t\t<SharedString name="Tags">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>
\t\t\t\t\t\t\t\t\t<UniqueId name="UniqueId">{uid_tex}</UniqueId>
\t\t\t\t\t\t\t\t</Properties>
\t\t\t\t\t\t\t</Item>
\t\t\t\t\t\t</Item>\n"""
        lines.append(part_xml)
    lines.append('\t\t\t\t\t</Item>\n')

lines.append('\t\t\t\t</Item>\n')
suelo_piso_0_xml = "".join(lines)
print(f"XML de Suelo_Piso_0 generado: {len(suelo_piso_0_xml)/1024/1024:.2f} MB ({len(chunks)} chunks, {global_part_idx} partes)")

# Escribir en streaming
print("Escribiendo archivo de salida en streaming...")
with open(OUT_RBXLX, 'r', encoding='utf-8', errors='ignore') as src, \
     open(TMP_RBXLX, 'w', encoding='utf-8') as dst:
    
    # 1. Encabezado previo a Suelo_Piso_0 (hasta linea 50438)
    for idx in range(1, 50439):
        line = src.readline()
        dst.write(line)
        
    # 2. Inyectar nuevo Suelo_Piso_0 chunked
    dst.write(suelo_piso_0_xml)
    
    # 3. Saltar viejo Suelo_Piso_0 (lineas 50439 a 1999387)
    for idx in range(50439, 1999388):
        src.readline()
        
    # 4. Escribir resto del archivo actualizando TerrenoCircundante si aplica
    terreno_updated = 0
    in_terreno = False
    for line in src:
        if 'name="Name">TerrenoCircundante<' in line:
            in_terreno = True
        if in_terreno and '<Y>-3.2</Y>' in line:
            line = line.replace('<Y>-3.2</Y>', '<Y>-3.5</Y>')
            terreno_updated += 1
            in_terreno = False
        dst.write(line)

print(f"Streaming finalizado. TerrenoCircundante ajustado: {terreno_updated}")

# Verificaciones de integridad
tmp_size = os.path.getsize(TMP_RBXLX) / 1024 / 1024
print(f"Tamano archivo generado: {tmp_size:.2f} MB")

with open(TMP_RBXLX, 'rb') as f:
    f.seek(-200, os.SEEK_END)
    tail = f.read().decode('utf-8', errors='ignore')
    if '</roblox>' in tail:
        print("Verificacion de cierre XML </roblox>: CORRECTO")
    else:
        raise RuntimeError("ERROR: El archivo XML no termina correctamente con </roblox>")

shutil.move(TMP_RBXLX, OUT_RBXLX)
print("Archivo PZ_Rosewood.rbxlx actualizado con exito!")
print(f"Tiempo total: {time.time() - t_start:.2f}s")

"""
Modulo de Vehiculos 3D para Project Zomboid B42 -> Roblox.
Exporta mallas de vehiculos y ruedas a formato Roblox .mesh (version 2.00)
e instancia vehiculos 3D (Policia, Bomberos, Civiles) en los estacionamientos de Rosewood.
"""
import os, struct, shutil
from pzlib.fbx_mesh import parse_ascii_fbx_mesh, write_roblox_mesh_v2
from pzlib import rbxlx as X

MEDIA = r'c:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media'

def parse_txt_mesh(path):
    """Parsea el formato legado .txt de Project Zomboid (media/models/Vehicles_Wheel.txt)."""
    lines = [l.strip() for l in open(path, 'r', encoding='utf-8', errors='ignore').readlines()]
    verts = []
    faces = []
    
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith('# Vertex Buffer:'):
            i += 1
            while i < len(lines) and not lines[i].startswith('#'):
                # 3 lineas por vertice: pos (x,y,z), normal (nx,ny,nz), uv (u,v)
                if i + 2 < len(lines):
                    p_parts = [float(x) for x in lines[i].split(',')]
                    n_parts = [float(x) for x in lines[i+1].split(',')]
                    uv_parts = [float(x) for x in lines[i+2].split(',')]
                    # Invertir Z para Roblox
                    verts.append((p_parts[0], p_parts[1], -p_parts[2], n_parts[0], n_parts[1], -n_parts[2], uv_parts[0], uv_parts[1]))
                    i += 3
                else:
                    break
        elif l.startswith('# Face Data:'):
            i += 1
            while i < len(lines) and not lines[i].startswith('#'):
                parts = [int(x.strip()) for x in lines[i].split(',') if x.strip()]
                if len(parts) == 3:
                    faces.append((parts[0], parts[1], parts[2]))
                i += 1
        else:
            i += 1
            
    return verts, faces

def prepare_vehicle_assets(out_dir):
    """Genera las mallas .mesh y copia las texturas de vehiculos necesarias."""
    mesh_dir = os.path.join(out_dir, 'meshes')
    tex_dir = os.path.join(out_dir, 'textures')
    os.makedirs(mesh_dir, exist_ok=True)
    os.makedirs(tex_dir, exist_ok=True)
    
    # 1. Rueda
    wheel_txt = os.path.join(MEDIA, 'models', 'Vehicles_Wheel.txt')
    wheel_mesh = os.path.join(mesh_dir, 'vehicle_wheel.mesh')
    if os.path.exists(wheel_txt) and not os.path.exists(wheel_mesh):
        v, f = parse_txt_mesh(wheel_txt)
        write_roblox_mesh_v2(wheel_mesh, v, f)
        
    wheel_tex = os.path.join(MEDIA, 'textures', 'Vehicles', 'vehicle_wheel.png')
    if os.path.exists(wheel_tex):
        shutil.copyfile(wheel_tex, os.path.join(tex_dir, 'vehicle_wheel.png'))
        
    # 2. Carros FBX
    v_models = {
        'police_car.mesh': ('Vehicles_CarNormalLights.fbx', 'vehicle_carlights_police.png'),
        'car_normal.mesh': ('Vehicles_CarNormal.fbx', 'vehicle_carnormal_blue.png'),
        'station_wagon.mesh': ('Vehicles_CarStationWagon.fbx', 'vehicle_carnormal_black.png'),
        'pickup_truck.mesh': ('Vehicles_PickUpTruck.fbx', 'vehicle_pickupfireshell.png'),
    }
    
    for mesh_name, (fbx_name, tex_name) in v_models.items():
        dst_m = os.path.join(mesh_dir, mesh_name)
        src_fbx = os.path.join(MEDIA, 'models_X', 'vehicles', fbx_name)
        if os.path.exists(src_fbx) and not os.path.exists(dst_m):
            v, f = parse_ascii_fbx_mesh(src_fbx)
            if v and f:
                write_roblox_mesh_v2(dst_m, v, f)
                
        src_tex = os.path.join(MEDIA, 'textures', 'Vehicles', tex_name)
        dst_tex = os.path.join(tex_dir, tex_name)
        if os.path.exists(src_tex) and not os.path.exists(dst_tex):
            shutil.copyfile(src_tex, dst_tex)

def create_vehicle_model(v_type, world_pos, angle_deg, tile_scale):
    """
    Crea un modelo de vehiculo 3D con chasis SpecialMesh y 4 ruedas SpecialMesh.
    v_type: 'police', 'fire', 'civilian', 'wagon'
    """
    import math
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    # Matriz de rotacion en Y
    R = [[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]]
    
    v_defs = {
        'police': ('police_car.mesh', 'vehicle_carlights_police.png', (255, 255, 255), 'Patrulla_Policial'),
        'fire': ('pickup_truck.mesh', 'vehicle_pickupfireshell.png', (255, 255, 255), 'Camioneta_Bomberos'),
        'civilian': ('car_normal.mesh', 'vehicle_carnormal_blue.png', (255, 255, 255), 'Auto_Sedan'),
        'wagon': ('station_wagon.mesh', 'vehicle_carnormal_black.png', (255, 255, 255), 'Auto_Familiar'),
    }
    
    mesh_file, tex_file, col, name_lbl = v_defs.get(v_type, v_defs['civilian'])
    
    m = X.Inst('Model', [('string', 'Name', name_lbl)])
    
    # 1. Chasis Part
    # El modelo FBX de PZ usa scale ~ 0.0145 * tile_scale
    chassis_size = (1.6 * tile_scale, 1.2 * tile_scale, 4.4 * tile_scale)
    chassis_pos = (world_pos[0], world_pos[1] + 0.65 * tile_scale, world_pos[2])
    
    chassis = X.part('Chasis', chassis_pos, R, chassis_size, color=col, material='SmoothPlastic', collide=True)
    # SpecialMesh
    smesh = X.Inst('SpecialMesh', [
        ('token', 'MeshType', 5), # FileMesh
        ('Content', 'MeshId', f'rbxasset://pz42/meshes/{mesh_file}'),
        ('Content', 'TextureId', f'rbxasset://pz42/textures/{tex_file}'),
        # FBX raw units are in cm (~330cm length), scaled down:
        ('Vector3', 'Scale', (0.0135 * tile_scale, 0.0135 * tile_scale, 0.0135 * tile_scale)),
        ('Vector3', 'Offset', (0, 0, 0)),
    ])
    chassis.add(smesh)
    
    # Luces delanteras
    light_l = X.Inst('PointLight', [
        ('Color3', 'Color', (1.0, 0.95, 0.8)),
        ('float', 'Range', 18.0),
        ('float', 'Brightness', 1.2),
        ('bool', 'Shadows', False)
    ])
    chassis.add(light_l)
    
    # Luces de sirena para policia / bomberos
    if v_type in ('police', 'fire'):
        siren_col = (0.2, 0.4, 1.0) if v_type == 'police' else (1.0, 0.2, 0.2)
        siren = X.Inst('PointLight', [
            ('Color3', 'Color', siren_col),
            ('float', 'Range', 25.0),
            ('float', 'Brightness', 2.0),
            ('bool', 'Shadows', False)
        ])
        chassis.add(siren)
        
    m.add(chassis)
    
    # 2. 4 Ruedas
    # Offsets relativos del chasis (ancho: +-0.66, alto: -0.55, largo: +1.55 y -1.11)
    wheel_offsets = [
        (0.66 * tile_scale, -0.32 * tile_scale, 1.45 * tile_scale),   # Delantera Izq
        (-0.66 * tile_scale, -0.32 * tile_scale, 1.45 * tile_scale),  # Delantera Der
        (0.66 * tile_scale, -0.32 * tile_scale, -1.15 * tile_scale),  # Trasera Izq
        (-0.66 * tile_scale, -0.32 * tile_scale, -1.15 * tile_scale), # Trasera Der
    ]
    
    for idx, (ox, oy, oz) in enumerate(wheel_offsets):
        # Rotar offset por R
        wx = chassis_pos[0] + (R[0][0]*ox + R[0][2]*oz)
        wy = chassis_pos[1] + oy
        wz = chassis_pos[2] + (R[2][0]*ox + R[2][2]*oz)
        
        w_part = X.part(f'Rueda_{idx}', (wx, wy, wz), R, (0.5 * tile_scale, 0.6 * tile_scale, 0.6 * tile_scale),
                        color=(30, 30, 30), material='SmoothPlastic', collide=False)
        w_mesh = X.Inst('SpecialMesh', [
            ('token', 'MeshType', 5),
            ('Content', 'MeshId', 'rbxasset://pz42/meshes/vehicle_wheel.mesh'),
            ('Content', 'TextureId', 'rbxasset://pz42/textures/vehicle_wheel.png'),
            ('Vector3', 'Scale', (1.82 * tile_scale * 0.9, 1.82 * tile_scale * 0.9, 1.82 * tile_scale * 0.9)),
        ])
        w_part.add(w_mesh)
        m.add(w_part)
        
    return m

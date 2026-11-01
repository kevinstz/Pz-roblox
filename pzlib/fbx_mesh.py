"""
Conversor de FBX ASCII de Project Zomboid a Roblox .mesh (version 2.00).
Corrige el indexado de UVIndex, normales por vertice de poligono y orientacion de caras hacia afuera.
"""
import struct, re, os

def parse_ascii_fbx_mesh(path, y_shift=0.0):
    text = open(path, 'r', encoding='utf-8', errors='ignore').read()
    
    # 1. Vertices (px, py, pz)
    m_v = re.search(r'Vertices:\s*\*\d+\s*\{\s*a:\s*([^}]+)\}', text)
    if not m_v: return None
    raw_v = [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', m_v.group(1))]
    vertices = [(raw_v[i], raw_v[i+1], raw_v[i+2]) for i in range(0, len(raw_v), 3)]
    
    # 2. Polygon vertex indices
    m_idx = re.search(r'PolygonVertexIndex:\s*\*\d+\s*\{\s*a:\s*([^}]+)\}', text)
    if not m_idx: return None
    poly_idx = [int(x) for x in re.findall(r'[-+]?\d+', m_idx.group(1))]
    
    # 3. Normals (ByPolygonVertex)
    m_n = re.search(r'LayerElementNormal:\s*0\s*\{([\s\S]*?)(?:LayerElement|\Z)', text)
    normals = []
    if m_n:
        raw_n = [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', re.search(r'Normals:\s*\*\d+\s*\{\s*a:\s*([^}]+)\}', m_n.group(1)).group(1))]
        normals = [(raw_n[i], raw_n[i+1], raw_n[i+2]) for i in range(0, len(raw_n), 3)]
        
    # 4. UVs y UVIndex (LayerElementUV: 0)
    m_uv0 = re.search(r'LayerElementUV:\s*0\s*\{([\s\S]*?)(?:LayerElementUV|LayerElementMaterial|\Z)', text)
    uvs = []
    uv_indices = []
    if m_uv0:
        uv0_text = m_uv0.group(1)
        m_uv = re.search(r'UV:\s*\*\d+\s*\{\s*a:\s*([^}]+)\}', uv0_text)
        if m_uv:
            raw_uv = [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', m_uv.group(1))]
            # Invertir V para formato DirectX / Roblox
            uvs = [(raw_uv[i], 1.0 - raw_uv[i+1]) for i in range(0, len(raw_uv), 2)]
        m_uvi = re.search(r'UVIndex:\s*\*\d+\s*\{\s*a:\s*([^}]+)\}', uv0_text)
        if m_uvi:
            uv_indices = [int(x) for x in re.findall(r'[-+]?\d+', m_uvi.group(1))]
            
    # 5. Triangular poligonos con winding exterior (0, k+1, k)
    faces = []
    current_poly = []
    for corner_idx, val in enumerate(poly_idx):
        is_end = val < 0
        v_idx = -val - 1 if is_end else val
        current_poly.append((v_idx, corner_idx))
        if is_end:
            for k in range(1, len(current_poly) - 1):
                faces.append((current_poly[0], current_poly[k+1], current_poly[k]))
            current_poly = []
            
    # 6. Transformar coordenadas de PZ/3dsMax (X: ancho, Y: largo, Z: arriba)
    # a Roblox (X: ancho, Y: arriba, Z: largo):
    # x_rbx = px
    # y_rbx = pz + y_shift
    # z_rbx = py
    unique_verts = {}
    out_verts = []
    out_faces = []
    
    for tri in faces:
        face_indices = []
        for v_idx, corner_idx in tri:
            px, py, pz = vertices[v_idx]
            x_rbx = px
            y_rbx = pz + y_shift
            z_rbx = py
            
            if corner_idx < len(normals):
                nx, ny, nz = normals[corner_idx]
            else:
                nx, ny, nz = (0.0, 1.0, 0.0)
            nx_rbx = nx
            ny_rbx = nz
            nz_rbx = ny
            
            if corner_idx < len(uv_indices) and uv_indices[corner_idx] < len(uvs):
                u, v = uvs[uv_indices[corner_idx]]
            elif v_idx < len(uvs):
                u, v = uvs[v_idx]
            else:
                u, v = (0.0, 0.0)
                
            key = (round(x_rbx, 4), round(y_rbx, 4), round(z_rbx, 4),
                   round(nx_rbx, 4), round(ny_rbx, 4), round(nz_rbx, 4),
                   round(u, 4), round(v, 4))
            if key not in unique_verts:
                idx = len(out_verts)
                unique_verts[key] = idx
                out_verts.append((x_rbx, y_rbx, z_rbx, nx_rbx, ny_rbx, nz_rbx, u, v))
            face_indices.append(unique_verts[key])
        out_faces.append(tuple(face_indices))
        
    return out_verts, out_faces

def write_roblox_mesh_v2(path, verts, faces):
    sz_hdr = 12
    sz_vert = 36
    sz_face = 12
    n_vert = len(verts)
    n_face = len(faces)
    
    with open(path, 'wb') as f:
        f.write(b'version 2.00\n')
        f.write(struct.pack('<HBBII', sz_hdr, sz_vert, sz_face, n_vert, n_face))
        for v in verts:
            px, py, pz, nx, ny, nz, tu, tv = v
            f.write(struct.pack('<8f4B', px, py, pz, nx, ny, nz, tu, tv, 0, 0, 0, 0))
        for face in faces:
            f.write(struct.pack('<3I', *face))

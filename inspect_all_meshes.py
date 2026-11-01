import struct, os

mesh_dir = r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\meshes'

for fname in os.listdir(mesh_dir):
    if not fname.endswith('.mesh'): continue
    path = os.path.join(mesh_dir, fname)
    with open(path, 'rb') as f:
        data = f.read()
    header_line = b'version 2.00\n'
    if not data.startswith(header_line):
        print(f"{fname}: not v2.00")
        continue
    rest = data[len(header_line):]
    cbSize, cbVertex, cbFace, numVertices, numFaces = struct.unpack_from('<HBBII', rest, 0)
    verts = []
    offset = cbSize
    for i in range(numVertices):
        x, y, z = struct.unpack_from('<fff', rest, offset)
        verts.append((x, y, z))
        offset += cbVertex
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    print(f"{fname:20s}: X=[{min(xs):.1f}, {max(xs):.1f}] ({max(xs)-min(xs):.1f}), Y=[{min(ys):.1f}, {max(ys):.1f}] ({max(ys)-min(ys):.1f}), Z=[{min(zs):.1f}, {max(zs):.1f}] ({max(zs)-min(zs):.1f})")

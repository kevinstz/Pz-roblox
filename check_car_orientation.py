import struct

with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\meshes\police_car.mesh', 'rb') as f:
    data = f.read()

header_line = b'version 2.00\n'
rest = data[len(header_line):]
cbSize, cbVertex, cbFace, numVertices, numFaces = struct.unpack_from('<HBBII', rest, 0)

verts = []
offset = cbSize
for i in range(numVertices):
    x, y, z, nx, ny, nz, u, v, _ = struct.unpack_from('<fffffffff', rest, offset)
    verts.append((x, y, z, nx, ny, nz, u, v))
    offset += cbVertex

# Let's inspect the extreme points:
# Max Z (41.9): What are the normals?
max_z_verts = [v for v in verts if v[2] > 35]
print(f"Verts with Z > 35 (count={len(max_z_verts)}):")
for v in max_z_verts[:5]:
    print(f"  pos=({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f}), norm=({v[3]:.2f}, {v[4]:.2f}, {v[5]:.2f})")

min_z_verts = [v for v in verts if v[2] < -40]
print(f"Verts with Z < -40 (count={len(min_z_verts)}):")
for v in min_z_verts[:5]:
    print(f"  pos=({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f}), norm=({v[3]:.2f}, {v[4]:.2f}, {v[5]:.2f})")

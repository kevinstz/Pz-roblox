import struct

with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\meshes\police_car.mesh', 'rb') as f:
    header = f.readline() # version 2.00\r\n
    num_verts_bytes = f.read(2)
    # in version 2.00, header has num_vertices and num_faces
    f.seek(0)
    content = f.read()

# Let's see the binary structure of Roblox mesh v2.00
# Header: "version 2.00\n"
# struct MeshHeader {
#   uint16_t cbSize; // 12
#   uint8_t cbVertex; // 40
#   uint8_t cbFace; // 12
#   uint16_t numLODs; // 0 or 1
#   uint32_t numVertices;
#   uint32_t numFaces;
# }
lines = content.split(b'\n', 1)
print("Header line:", lines[0])
rest = lines[1]
cbSize, cbVertex, cbFace, numLODs, numVertices, numFaces = struct.unpack_from('<HBBHII', rest, 0)
print(f"cbSize={cbSize}, cbVertex={cbVertex}, cbFace={cbFace}, numLODs={numLODs}, numVertices={numVertices}, numFaces={numFaces}")

# Each vertex is cbVertex bytes: 3 floats (pos), 3 floats (norm), 2 or 3 floats (uv)
verts = []
offset = cbSize
for i in range(numVertices):
    x, y, z = struct.unpack_from('<fff', rest, offset)
    verts.append((x, y, z))
    offset += cbVertex

xs = [v[0] for v in verts]
ys = [v[1] for v in verts]
zs = [v[2] for v in verts]

print(f"Mesh Vertices Bounding Box:")
print(f"  X: [{min(xs):.2f}, {max(xs):.2f}] -> range = {max(xs)-min(xs):.2f}")
print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}] -> range = {max(ys)-min(ys):.2f}")
print(f"  Z: [{min(zs):.2f}, {max(zs):.2f}] -> range = {max(zs)-min(zs):.2f}")

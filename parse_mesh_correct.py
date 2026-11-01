import struct

with open(r'C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\meshes\police_car.mesh', 'rb') as f:
    data = f.read()

header_line = b'version 2.00\n'
rest = data[len(header_line):]

cbSize, cbVertex, cbFace, numVertices, numFaces = struct.unpack_from('<HBBII', rest, 0)
print(f"cbSize={cbSize}, cbVertex={cbVertex}, cbFace={cbFace}, numVertices={numVertices}, numFaces={numFaces}")

verts = []
offset = cbSize
for i in range(numVertices):
    x, y, z = struct.unpack_from('<fff', rest, offset)
    verts.append((x, y, z))
    offset += cbVertex

xs = [v[0] for v in verts]
ys = [v[1] for v in verts]
zs = [v[2] for v in verts]

print(f"police_car.mesh Bounding Box:")
print(f"  X: [{min(xs):.2f}, {max(xs):.2f}] -> range = {max(xs)-min(xs):.2f}")
print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}] -> range = {max(ys)-min(ys):.2f}")
print(f"  Z: [{min(zs):.2f}, {max(zs):.2f}] -> range = {max(zs)-min(zs):.2f}")

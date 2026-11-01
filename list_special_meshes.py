with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

mesh_indices = [m.start() for m in re.finditer(r'<Item class="SpecialMesh"', text)]
print(f"Total SpecialMesh instances: {len(mesh_indices)}")
for idx in mesh_indices:
    part_idx = text.rfind('<Item class="Part"', 0, idx)
    part_block = text[part_idx:idx+800]
    m_name = re.search(r'<string name="Name">([^<]+)</string>', part_block)
    name = m_name.group(1) if m_name else "?"
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', part_block, re.DOTALL)
    pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else "?"
    m_mesh = re.search(r'<Content name="MeshId"><url>([^<]+)</url></Content>', text[idx:idx+800])
    mesh_id = m_mesh.group(1) if m_mesh else "?"
    print(f"Name={name:30s} | Pos={pos} | MeshId={mesh_id}")

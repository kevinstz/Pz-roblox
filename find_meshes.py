# Search for MeshPart or UnionOperation in PZ_Rosewood.rbxlx
with open("out/PZ_Rosewood.rbxlx", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

meshparts = re.findall(r'<Item class="(MeshPart|UnionOperation)" referent="([^"]+)">', text)
print(f"Total MeshPart / UnionOperation: {len(meshparts)}")
for cls, ref in meshparts:
    idx = text.find(f'referent="{ref}"')
    block = text[idx:idx+1500]
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    name = m_name.group(1) if m_name else "?"
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else "?"
    print(f"Ref={ref} | Class={cls} | Name={name} | Pos={pos}")

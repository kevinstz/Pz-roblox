import re

with open('out/PZ_Rosewood.rbxlx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search for MeshPart
meshparts = re.findall(r'<Item class="MeshPart" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
print(f"Total MeshParts: {len(meshparts)}")
for ref, block in meshparts:
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_cf = re.search(r'<CoordinateFrame name="CFrame">.*?<X>([^<]+)</X>.*?<Y>([^<]+)</Y>.*?<Z>([^<]+)</Z>', block, re.DOTALL)
    pos = (float(m_cf.group(1)), float(m_cf.group(2)), float(m_cf.group(3))) if m_cf else None
    print(f"MeshPart: Ref={ref} | Name={m_name.group(1) if m_name else ''} | Pos={pos}")

# Let's search for SpecialMesh
specialmeshes = re.findall(r'<Item class="SpecialMesh" referent="([^"]+)">(.*?)</Item>', text, re.DOTALL)
print(f"Total SpecialMeshes: {len(specialmeshes)}")
for ref, block in specialmeshes[:30]:
    m_name = re.search(r'<string name="Name">([^<]+)</string>', block)
    m_id = re.search(r'<Content name="MeshId">.*?<url>([^<]+)</url>', block, re.DOTALL)
    print(f"SpecialMesh: Ref={ref} | Name={m_name.group(1) if m_name else ''} | MeshId={m_id.group(1) if m_id else ''}")

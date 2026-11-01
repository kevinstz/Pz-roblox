from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

edge_parts = [p for p in found if -55 <= p[2] <= -45 and -74 <= p[4] <= -60 and 6.0 <= p[3] <= 12.5]
print(f"Total parts on lower roof edge: {len(edge_parts)}")
for p in sorted(edge_parts, key=lambda x: (x[4], x[3], x[2])):
    m_s = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', p[6])
    sz = f"({float(m_s.group(1)):.2f}, {float(m_s.group(2)):.2f}, {float(m_s.group(3)):.2f})" if m_s else "?"
    m_col = re.search(r'<Color3uint8 name="Color3uint8">(\d+)</Color3uint8>', p[6])
    col = m_col.group(1) if m_col else "?"
    m_tr = re.search(r'<float name="Transparency">([^<]+)</float>', p[6])
    tr = m_tr.group(1) if m_tr else "0"
    decals = re.findall(r'<Texture><url>([^<]+)</url></Texture>', p[6])
    print(f"Ref={p[7]} | Cls={p[1]:10s} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Sz={sz} | Tr={tr} | Col={col} | Decals={len(decals)} | Parent={p[5]}")

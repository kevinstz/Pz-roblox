from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

for p in found:
    if -55 <= p[2] <= -40 and -70 <= p[4] <= -55 and 0 <= p[3] <= 12:
        txt = p[6]
        # extract size
        m_size = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', txt)
        size_str = f"({m_size.group(1)}, {m_size.group(2)}, {m_size.group(3)})" if m_size else "?"
        # extract color
        m_col = re.search(r'<Color3uint8 name="Color3uint8">(\d+)</Color3uint8>', txt)
        col_str = m_col.group(1) if m_col else "?"
        # extract decals / textures
        decals = re.findall(r'<Texture><url>([^<]+)</url></Texture>', txt)
        decal_names = re.findall(r'<string name="Name">([^<]+)</string>', txt)
        print(f"Ref={p[7]} | Name={p[0]} | Class={p[1]} | Pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Size={size_str} | Col={col_str} | Decals={len(decals)} | Parent={p[5]}")

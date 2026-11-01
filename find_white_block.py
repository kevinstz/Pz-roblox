from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

print("All parts in region X in [-54, -45], Z in [-66, -56], Y in [0, 8]:")
for p in found:
    if -54 <= p[2] <= -45 and -66 <= p[4] <= -56 and 0 <= p[3] <= 8:
        # extract size
        m_s = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', p[6])
        size = f"({m_s.group(1)}, {m_s.group(2)}, {m_s.group(3)})" if m_s else "?"
        m_c = re.search(r'<Color3uint8 name="Color3uint8">(\d+)</Color3uint8>', p[6])
        col = m_c.group(1) if m_c else "?"
        # check decals
        decals = re.findall(r'<url>([^<]+)</url>', p[6])
        print(f"Ref={p[7]} | Name={p[0]} | Pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Size={size} | Col={col} | Decals={decals} | Parent={p[5]}")

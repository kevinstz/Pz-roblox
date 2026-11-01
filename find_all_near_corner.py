from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

parts = [p for p in found if -60 <= p[2] <= -40 and -70 <= p[4] <= -50 and 0 <= p[3] <= 20]
print(f"Total parts in box: {len(parts)}")
for p in sorted(parts, key=lambda x: (x[3], x[4], x[2])):
    # size
    m_s = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', p[6])
    sz = f"({float(m_s.group(1)):.2f}, {float(m_s.group(2)):.2f}, {float(m_s.group(3)):.2f})" if m_s else "?"
    print(f"Ref={p[7]} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Sz={sz} | Parent={p[5]}")

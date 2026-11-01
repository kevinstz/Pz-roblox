from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

for p in found:
    if -65 <= p[2] <= -35 and -75 <= p[4] <= -45:
        txt = p[6]
        m_col = re.search(r'<Color3uint8 name="Color3uint8">(\d+)</Color3uint8>', txt)
        col = int(m_col.group(1)) if m_col else None
        m_s = re.search(r'<Vector3 name="size">\s*<X>([^<]+)</X>\s*<Y>([^<]+)</Y>\s*<Z>([^<]+)</Z>', txt)
        sz = (float(m_s.group(1)), float(m_s.group(2)), float(m_s.group(3))) if m_s else (0,0,0)
        # Check if color is white-ish or light blue:
        # 0xFFFFFFFF = 4294967295
        decals = re.findall(r'<Texture><url>([^<]+)</url></Texture>', txt)
        # If part has height > 3 and width > 1:
        if sz[1] > 2.0 or sz[0] > 2.0 or sz[2] > 2.0:
            # check if it mentions door or arch or frame or decoration or sign
            print(f"Ref={p[7]} | Name={p[0]:28s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Sz=({sz[0]:.2f}, {sz[1]:.2f}, {sz[2]:.2f}) | Col={col} | Decals={decals}")

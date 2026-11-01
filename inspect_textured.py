from dump_pair2_region import dump_pair2_region
import re

found = dump_pair2_region()

for p in found:
    if -55 <= p[2] <= -40 and -70 <= p[4] <= -55:
        txt = p[6]
        if 'Decal' in txt or 'Texture' in txt:
            # find texture name/id
            tex = re.findall(r'<url>([^<]+)</url>', txt)
            print(f"Textured part: Ref={p[7]} | Name={p[0]} | Pos=({p[2]:.2f}, {p[3]:.2f}, {p[4]:.2f}) | Tex={tex} | Parent={p[5]}")

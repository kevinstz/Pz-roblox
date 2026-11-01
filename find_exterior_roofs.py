from dump_pair2_region import dump_pair2_region

found = dump_pair2_region()

for p in found:
    if 'walls_exterior_roofs' in p[0] and -55 <= p[2] <= -40 and -80 <= p[4] <= -60:
        print(f"Ref={p[7]} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Parent={p[5]}")

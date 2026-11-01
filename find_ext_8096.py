from dump_pair2_region import dump_pair2_region

found = dump_pair2_region()

for p in found:
    if any(k in p[5] for k in ['Exterior_8096_11632', 'Exterior_8096_11648', 'Exterior_8096_11664']):
        print(f"Ref={p[7]} | Name={p[0]:30s} | Pos=({p[2]:6.2f}, {p[3]:5.2f}, {p[4]:6.2f}) | Parent={p[5]}")
